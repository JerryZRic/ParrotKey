import os
import queue
import subprocess
import threading
import time

import numpy as np
import sounddevice as sd
import torch
from pynput import keyboard

from parrotkey.asr.qwen_pt import QwenPtAsrBackend
from parrotkey.config import AppConfig
from parrotkey.inject.clipboard import ClipboardInjector


def run_push_to_talk_app(config: AppConfig) -> None:
    backend = QwenPtAsrBackend(config)
    injector = ClipboardInjector(config)
    hotkey = keyboard.Key.ctrl_r
    app_name = "ParrotKey"

    backend.warmup()

    is_recording = False
    recording_chunks: list[np.ndarray] = []
    record_lock = threading.Lock()
    work_queue: queue.Queue[np.ndarray] = queue.Queue()

    def play_beep(path: str) -> None:
        if not config.enable_beep or not os.path.exists(path):
            return
        try:
            subprocess.Popen(
                ["paplay", path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass

    def notify(title: str, body: str = "") -> None:
        if not config.enable_notify:
            return
        try:
            subprocess.Popen(
                ["notify-send", title, body],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass

    def audio_callback(indata, frames, time_info, status) -> None:
        del frames, time_info
        nonlocal recording_chunks
        if status:
            print("audio status:", status)
        with record_lock:
            if is_recording:
                recording_chunks.append(indata.copy())

    print("默認設備:", sd.default.device)
    print("可用設備:")
    print(sd.query_devices())
    print("PyTorch 線程:", torch.get_num_threads())

    stream = sd.InputStream(
        samplerate=config.sample_rate,
        channels=config.input_channels,
        dtype="float32",
        callback=audio_callback,
        blocksize=0,
        device=config.input_device,
    )
    stream.start()

    def worker() -> None:
        while True:
            audio = work_queue.get()
            try:
                t0 = time.time()
                text = backend.transcribe(audio)
                dt = time.time() - t0
                print(f"識別耗時: {dt:.2f}s")
                print("識別結果:", repr(text))

                if text:
                    injector.paste_text_preserve_clipboard(text)
                    play_beep(config.beep_done)
                    notify(app_name, f"已輸入：{text[:30]}")
                else:
                    play_beep(config.beep_error)
                    notify(app_name, "識別為空")
            except Exception as exc:
                print("識別失敗:", exc)
                play_beep(config.beep_error)
                notify(app_name, f"識別失敗：{exc}")
            finally:
                work_queue.task_done()

    threading.Thread(target=worker, daemon=True).start()

    def on_press(key) -> None:
        nonlocal is_recording, recording_chunks
        if key == hotkey and not is_recording:
            with record_lock:
                recording_chunks = []
                is_recording = True
            print("🎤 開始錄音")
            play_beep(config.beep_start)
            notify(app_name, "開始錄音")

    def on_release(key) -> None:
        nonlocal is_recording, recording_chunks
        if key == hotkey and is_recording:
            with record_lock:
                is_recording = False
                chunks = recording_chunks[:]
                recording_chunks = []

            if not chunks:
                print("冇錄到音頻")
                play_beep(config.beep_error)
                notify(app_name, "冇錄到音頻")
                return

            audio = np.concatenate(chunks, axis=0)
            print(f"🛑 停止錄音，音頻形狀: {audio.shape}")
            notify(app_name, "正在識別...")
            work_queue.put(audio)

    print("✅ 已啟動：按住右 Ctrl 講嘢，鬆開後自動貼到當前光標處")
    print("⚠️ 當前模型:", config.model_path)
    print("⚠️ 當前輸入設備:", config.input_device, "通道數:", config.input_channels)
    print("⚠️ 當前語言:", config.language)
    print("⚠️ max_new_tokens:", config.max_new_tokens)

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()
