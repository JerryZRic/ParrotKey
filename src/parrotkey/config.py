from dataclasses import dataclass


@dataclass(slots=True)
class AppConfig:
    model_path: str
    sample_rate: int = 16000
    input_device: str = "pulse"
    input_channels: int = 4
    language: str | None = "Chinese"
    max_new_tokens: int = 96
    paste_delay_sec: float = 0.12
    restore_delay_sec: float = 0.18
    min_rms: float = 1e-4
    save_debug_wav: bool = False
    enable_beep: bool = True
    enable_notify: bool = True
    omp_num_threads: str = "6"
    mkl_num_threads: str = "6"
    torch_num_threads: int = 6
    torch_num_interop_threads: int = 1
    beep_start: str = "/usr/share/sounds/freedesktop/stereo/message.oga"
    beep_done: str = "/usr/share/sounds/freedesktop/stereo/complete.oga"
    beep_error: str = "/usr/share/sounds/freedesktop/stereo/dialog-warning.oga"
