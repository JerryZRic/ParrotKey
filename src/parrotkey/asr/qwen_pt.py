import os

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import numpy as np
import torch
from qwen_asr import Qwen3ASRModel

from parrotkey.config import AppConfig


class QwenPtAsrBackend:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        os.environ["OMP_NUM_THREADS"] = config.omp_num_threads
        os.environ["MKL_NUM_THREADS"] = config.mkl_num_threads
        torch.set_num_threads(config.torch_num_threads)
        torch.set_num_interop_threads(config.torch_num_interop_threads)

        print("正在加載模型...")
        self.asr = Qwen3ASRModel.from_pretrained(
            config.model_path,
            dtype=torch.float32,
            device_map="cpu",
            max_new_tokens=config.max_new_tokens,
        )
        self.asr.model.generation_config.pad_token_id = 151645
        print("模型加載完成")

    def warmup(self) -> None:
        dummy = np.zeros(int(self.config.sample_rate * 0.3), dtype=np.float32)
        try:
            _ = self.asr.transcribe(
                audio=(dummy, self.config.sample_rate),
                language=self.config.language,
                return_time_stamps=False,
            )
            print("預熱完成")
        except Exception as exc:
            print("預熱失敗，但唔影響繼續使用:", exc)

    def transcribe(self, audio: np.ndarray) -> str:
        if audio.size == 0:
            return ""

        if audio.ndim == 2:
            rms_per_channel = np.sqrt(np.mean(audio ** 2, axis=0))
            best_ch = int(np.argmax(rms_per_channel))
            print("各通道 RMS:", rms_per_channel, "選中通道:", best_ch)
            audio = audio[:, best_ch]

        audio = audio.astype(np.float32, copy=False)

        max_abs = float(np.max(np.abs(audio))) if audio.size else 0.0
        rms = float(np.sqrt(np.mean(audio ** 2))) if audio.size else 0.0
        print(f"音頻電平: max={max_abs:.6f}, rms={rms:.6f}")

        if rms < self.config.min_rms:
            return ""

        if self.config.save_debug_wav:
            self._save_debug_wav(audio)

        with torch.inference_mode():
            results = self.asr.transcribe(
                audio=(audio, self.config.sample_rate),
                language=self.config.language,
                return_time_stamps=False,
            )

        if not results:
            return ""

        text = results[0].text or ""
        return " ".join(text.split()).strip()

    def _save_debug_wav(self, audio: np.ndarray) -> None:
        try:
            import soundfile as sf

            sf.write("debug_record.wav", audio, self.config.sample_rate)
            print("已保存 debug_record.wav")
        except Exception as exc:
            print("保存 debug wav 失敗:", exc)
