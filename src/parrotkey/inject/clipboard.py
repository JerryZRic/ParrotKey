import subprocess
import time

from parrotkey.config import AppConfig


class ClipboardInjector:
    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def paste_text_preserve_clipboard(self, text: str) -> None:
        if not text:
            return

        old_clipboard = self._get_clipboard_text()
        if not self._set_clipboard_text(text):
            return

        time.sleep(self.config.paste_delay_sec)
        subprocess.run(
            ["xdotool", "key", "--clearmodifiers", "ctrl+v"],
            check=False,
        )
        time.sleep(self.config.restore_delay_sec)

        if old_clipboard is not None:
            self._set_clipboard_text(old_clipboard)

    def _get_clipboard_text(self) -> str | None:
        try:
            result = subprocess.run(
                ["xclip", "-selection", "clipboard", "-o"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            if result.returncode != 0:
                return None
            return result.stdout.decode("utf-8", errors="ignore")
        except Exception:
            return None

    def _set_clipboard_text(self, text: str) -> bool:
        try:
            subprocess.run(
                ["xclip", "-selection", "clipboard"],
                input=text.encode("utf-8"),
                check=True,
            )
            return True
        except Exception as exc:
            print("寫入剪貼板失敗:", exc)
            return False
