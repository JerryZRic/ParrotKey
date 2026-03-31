# ParrotKey

ParrotKey is a local push-to-talk voice typing framework.

Hold a key, speak, release, and text appears.

## What It Does

- Captures microphone input while a hotkey is held
- Runs local speech recognition on release
- Inserts recognized text into the active application
- Keeps the architecture open for multiple ASR backends and injection modes

## Current Status

The first prototype is included.

Today it focuses on a Linux desktop workflow with:

- `Right Ctrl` push-to-talk
- Local `Qwen3-ASR` inference through PyTorch on CPU
- Clipboard-based paste into the active window
- Optional beeps and desktop notifications

## Project Goals

- Run locally and keep voice data on your machine
- Support push-to-talk voice input on desktop systems
- Stay backend-agnostic so different ASR engines can plug in
- Make text insertion flexible: paste, simulated typing, IME integrations
- Leave room for optional post-processing with local LLMs

## Planned Architecture

- `parrotkey.audio`: microphone capture and buffering
- `parrotkey.hotkey`: global hotkey handling
- `parrotkey.asr`: ASR backend adapters
- `parrotkey.inject`: text insertion backends
- `parrotkey.pipeline`: end-to-end voice typing flow

## Initial Scope

- Linux desktop focus
- Push-to-talk interaction
- Local ASR backend support
- Clipboard paste or simulated typing output

## Quick Start

The current runnable prototype mirrors the original local input script:

- Hold `Right Ctrl` to record
- Release to transcribe
- Paste recognized text into the active window
- Use Qwen3-ASR on CPU through PyTorch

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the package:

```bash
pip install -e .
pip install -r requirements.txt
```

Run ParrotKey:

```bash
parrotkey --model-path /path/to/Qwen3-ASR-0.6B
```

Or without installation:

```bash
PYTHONPATH=src python3 -m parrotkey --model-path /path/to/Qwen3-ASR-0.6B
```

System tools currently expected on Linux:

- `xclip`
- `xdotool`
- `paplay`
- `notify-send`

## Development

The current codebase is organized as a package under `src/parrotkey`, with the first prototype already split into config, ASR backend, text injection, and pipeline modules.

## Roadmap

- Add more ASR backends behind a shared interface
- Define a backend interface for ASR engines
- Add an output interface for different text injection modes
- Add configuration and logging
- Explore faster local backends and streaming support

## License

See [LICENSE](LICENSE).
