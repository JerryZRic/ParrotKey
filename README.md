# ParrotKey

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [粵語](README.yue.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform: Linux](https://img.shields.io/badge/platform-Linux-blue.svg)](README.md)
[![Prototype](https://img.shields.io/badge/status-prototype-orange.svg)](README.md)
[![Hugging Face Qwen3-ASR-0.6B](https://img.shields.io/badge/model-Qwen3--ASR--0.6B-yellow.svg)](https://huggingface.co/Qwen/Qwen3-ASR-0.6B)

ParrotKey is a local push-to-talk voice typing framework.

Hold a key, speak, release, and text appears.

ParrotKey is designed as a backend-agnostic foundation for local voice typing tools, starting from a Linux prototype built around Qwen3-ASR.

## Contents

- [What It Does](#what-it-does)
- [Current Status](#current-status)
- [Quick Start](#quick-start)
- [Model](#model)
- [Run as a User Service](#run-as-a-user-service)
- [Repository Layout](#repository-layout)
- [Roadmap](#roadmap)

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

## Model

The current prototype expects a local copy of `Qwen3-ASR-0.6B`.

Official Hugging Face model page:

https://huggingface.co/Qwen/Qwen3-ASR-0.6B

Example download command:

```bash
huggingface-cli download Qwen/Qwen3-ASR-0.6B --local-dir /path/to/Qwen3-ASR-0.6B
```

## Run as a User Service

If you want ParrotKey to stay available after login, run it as a `systemd --user` service.

An example unit file is included at `examples/parrotkey.service`.

1. Create the user service directory:

```bash
mkdir -p ~/.config/systemd/user
```

2. Copy the example service file:

```bash
cp examples/parrotkey.service ~/.config/systemd/user/parrotkey.service
```

3. Edit the service file and update:

- `WorkingDirectory`
- `Environment=PATH=...`
- `ExecStart`
- `--model-path`

4. Reload and start the service:

```bash
systemctl --user daemon-reload
systemctl --user enable --now parrotkey.service
```

5. Check logs if needed:

```bash
journalctl --user -u parrotkey.service -f
```

Notes:

- This prototype currently depends on desktop session tools such as `xclip`, `xdotool`, `paplay`, and `notify-send`.
- The included example assumes an X11-style desktop session because clipboard paste is done through `xdotool` and `xclip`.
- Depending on your desktop environment, you may need to keep `DISPLAY`, `XAUTHORITY`, `DBUS_SESSION_BUS_ADDRESS`, or `XDG_RUNTIME_DIR` available in the user service environment.

## Repository Layout

- `src/parrotkey/asr`: ASR backend adapters
- `src/parrotkey/audio`: audio capture utilities
- `src/parrotkey/hotkey`: hotkey handling
- `src/parrotkey/inject`: text injection backends
- `src/parrotkey/pipeline`: end-to-end voice typing flow
- `examples`: service and deployment examples

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
