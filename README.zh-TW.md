# ParrotKey

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [粵語](README.yue.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform: Linux](https://img.shields.io/badge/platform-Linux-blue.svg)](README.md)
[![Prototype](https://img.shields.io/badge/status-prototype-orange.svg)](README.md)
[![Hugging Face Qwen3-ASR-0.6B](https://img.shields.io/badge/model-Qwen3--ASR--0.6B-yellow.svg)](https://huggingface.co/Qwen/Qwen3-ASR-0.6B)

ParrotKey 是一個本地的按鍵通話式語音輸入框架。

按住一個鍵，開口說話，放開之後，文字就會出現。

ParrotKey 的目標是成為與後端無關的本地語音輸入基礎框架，而目前第一版從基於 Qwen3-ASR 的 Linux 原型開始。

## 目錄

- [它可以做什麼](#它可以做什麼)
- [目前狀態](#目前狀態)
- [快速開始](#快速開始)
- [模型](#模型)
- [作為使用者服務執行](#作為使用者服務執行)
- [倉庫結構](#倉庫結構)
- [路線圖](#路線圖)

## 它可以做什麼

- 在按住熱鍵時擷取麥克風音訊
- 放開按鍵後執行語音辨識
- 將辨識出的文字插入目前作用中的應用程式
- 保持後端與文字注入方式可擴充

## 目前狀態

第一個原型已經包含在倉庫裡。

目前主要面向 Linux 桌面工作流程，支援：

- 按住 `Right Ctrl` 說話
- 透過 PyTorch 在 CPU 上執行本地 `Qwen3-ASR`
- 透過剪貼簿貼上到目前視窗
- 可選提示音與桌面通知

## 專案目標

- 本地執行，讓語音資料留在你的電腦上
- 支援桌面系統上的按鍵通話式語音輸入
- 保持 ASR 後端無關，方便接入不同模型
- 讓文字注入方式更靈活，例如貼上、模擬輸入、IME 整合
- 為本地 LLM 後處理預留空間

## 規劃中的架構

- `parrotkey.audio`：麥克風擷取與緩衝
- `parrotkey.hotkey`：全域熱鍵處理
- `parrotkey.asr`：ASR 後端適配層
- `parrotkey.inject`：文字注入後端
- `parrotkey.pipeline`：端到端語音輸入流程

## 初始範圍

- 以 Linux 桌面為主
- 按鍵通話互動
- 本地 ASR 後端支援
- 剪貼簿貼上或模擬輸入輸出

## 快速開始

目前可執行的原型延續了原本的本地輸入腳本：

- 按住 `Right Ctrl` 開始錄音
- 放開後進行辨識
- 把辨識文字貼到目前作用中的視窗
- 使用 CPU + PyTorch 版本的 Qwen3-ASR

建立並啟用虛擬環境：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

安裝專案：

```bash
pip install -e .
pip install -r requirements.txt
```

執行 ParrotKey：

```bash
parrotkey --model-path /path/to/Qwen3-ASR-0.6B
```

如果不安裝，也可以這樣執行：

```bash
PYTHONPATH=src python3 -m parrotkey --model-path /path/to/Qwen3-ASR-0.6B
```

目前 Linux 需要的系統工具：

- `xclip`
- `xdotool`
- `paplay`
- `notify-send`

## 模型

目前原型需要本地準備一份 `Qwen3-ASR-0.6B`。

官方 Hugging Face 頁面：

https://huggingface.co/Qwen/Qwen3-ASR-0.6B

下載範例：

```bash
huggingface-cli download Qwen/Qwen3-ASR-0.6B --local-dir /path/to/Qwen3-ASR-0.6B
```

## 作為使用者服務執行

如果你希望 ParrotKey 在登入後常駐執行，建議使用 `systemd --user` 服務。

範例 unit 檔位於 `examples/parrotkey.service`。

1. 建立使用者服務目錄：

```bash
mkdir -p ~/.config/systemd/user
```

2. 複製範例服務檔：

```bash
cp examples/parrotkey.service ~/.config/systemd/user/parrotkey.service
```

3. 編輯服務檔，並修改以下項目：

- `WorkingDirectory`
- `Environment=PATH=...`
- `ExecStart`
- `--model-path`

4. 重新載入並啟動服務：

```bash
systemctl --user daemon-reload
systemctl --user enable --now parrotkey.service
```

5. 如需查看日誌：

```bash
journalctl --user -u parrotkey.service -f
```

注意：

- 目前原型依賴 `xclip`、`xdotool`、`paplay` 與 `notify-send` 這類桌面工作階段工具。
- 內附範例服務以 X11 風格桌面工作階段為前提，因為目前文字插入方式仰賴 `xdotool` 與 `xclip`。
- 依桌面環境不同，可能還需要讓使用者服務取得 `DISPLAY`、`XAUTHORITY`、`DBUS_SESSION_BUS_ADDRESS` 或 `XDG_RUNTIME_DIR`。

## 倉庫結構

- `src/parrotkey/asr`：ASR 後端適配層
- `src/parrotkey/audio`：音訊擷取工具
- `src/parrotkey/hotkey`：熱鍵處理
- `src/parrotkey/inject`：文字注入後端
- `src/parrotkey/pipeline`：端到端語音輸入流程
- `examples`：服務與部署範例

## 開發說明

目前程式碼位於 `src/parrotkey` 套件下，第一版原型已拆分為設定、ASR 後端、文字注入與主流程模組。

## 路線圖

- 在共同介面下接入更多 ASR 後端
- 定義清楚的 ASR 後端介面
- 增加不同文字注入方式的介面
- 增加設定與日誌能力
- 探索更快的本地後端與串流支援

## 授權

請見 [LICENSE](LICENSE)。
