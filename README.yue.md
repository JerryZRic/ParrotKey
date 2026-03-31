# ParrotKey

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [粵語](README.yue.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform: Linux](https://img.shields.io/badge/platform-Linux-blue.svg)](README.md)
[![Prototype](https://img.shields.io/badge/status-prototype-orange.svg)](README.md)
[![Hugging Face Qwen3-ASR-0.6B](https://img.shields.io/badge/model-Qwen3--ASR--0.6B-yellow.svg)](https://huggingface.co/Qwen/Qwen3-ASR-0.6B)

ParrotKey 係一個本地嘅按鍵通話式語音輸入框架。

撳住一個鍵，講一句，放手之後，文字就會出現。

ParrotKey 想做成一個同後端無關嘅本地語音輸入基礎框架，而家第一版就由基於 Qwen3-ASR 嘅 Linux 原型開始。

## 目錄

- [佢做到啲乜](#佢做到啲乜)
- [而家狀態](#而家狀態)
- [快速開始](#快速開始)
- [模型](#模型)
- [以使用者服務運行](#以使用者服務運行)
- [倉庫結構](#倉庫結構)
- [路線圖](#路線圖)

## 佢做到啲乜

- 撳住熱鍵嗰陣收咪高峰音訊
- 放開按鍵之後做語音識別
- 將識別結果插入去而家用緊嘅應用程式
- 保持後端同文字注入方式都可以繼續擴展

## 而家狀態

第一個原型已經放咗入倉庫。

而家主要針對 Linux 桌面流程，支援：

- 撳住 `Right Ctrl` 講嘢
- 經 PyTorch 喺 CPU 上跑本地 `Qwen3-ASR`
- 用剪貼板貼返去目前視窗
- 可選提示聲同桌面通知

## 項目目標

- 本地運行，令語音資料留喺你部機度
- 支援桌面系統嘅按鍵通話式語音輸入
- 保持 ASR 後端無關，方便接唔同模型
- 令文字注入方式更靈活，例如貼上、模擬打字、IME 整合
- 為本地 LLM 後處理預留空間

## 規劃中架構

- `parrotkey.audio`：咪高峰錄音同緩衝
- `parrotkey.hotkey`：全域熱鍵處理
- `parrotkey.asr`：ASR 後端適配層
- `parrotkey.inject`：文字注入後端
- `parrotkey.pipeline`：端到端語音輸入流程

## 初期範圍

- 以 Linux 桌面為主
- 按鍵通話互動
- 本地 ASR 後端支援
- 剪貼板貼上或者模擬輸入輸出

## 快速開始

而家可以跑嘅原型，基本上沿用咗原本個本地輸入腳本：

- 撳住 `Right Ctrl` 開始錄音
- 放手之後做識別
- 將識別文字貼去目前作用中視窗
- 使用 CPU + PyTorch 版本 Qwen3-ASR

建立並啟動虛擬環境：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

安裝項目：

```bash
pip install -e .
pip install -r requirements.txt
```

執行 ParrotKey：

```bash
parrotkey --model-path /path/to/Qwen3-ASR-0.6B
```

如果唔安裝，都可以咁樣跑：

```bash
PYTHONPATH=src python3 -m parrotkey --model-path /path/to/Qwen3-ASR-0.6B
```

目前 Linux 需要嘅系統工具：

- `xclip`
- `xdotool`
- `paplay`
- `notify-send`

## 模型

而家個原型需要你本地準備一份 `Qwen3-ASR-0.6B`。

官方 Hugging Face 頁面：

https://huggingface.co/Qwen/Qwen3-ASR-0.6B

下載例子：

```bash
huggingface-cli download Qwen/Qwen3-ASR-0.6B --local-dir /path/to/Qwen3-ASR-0.6B
```

## 以使用者服務運行

如果你想 ParrotKey 登入之後就常駐運行，建議用 `systemd --user` 服務。

示例 unit 檔放喺 `examples/parrotkey.service`。

1. 建立使用者服務目錄：

```bash
mkdir -p ~/.config/systemd/user
```

2. 複製示例服務檔：

```bash
cp examples/parrotkey.service ~/.config/systemd/user/parrotkey.service
```

3. 編輯服務檔，並修改以下內容：

- `WorkingDirectory`
- `Environment=PATH=...`
- `ExecStart`
- `--model-path`

4. 重新載入同啟動服務：

```bash
systemctl --user daemon-reload
systemctl --user enable --now parrotkey.service
```

5. 如果要睇日誌：

```bash
journalctl --user -u parrotkey.service -f
```

注意：

- 而家個原型依賴 `xclip`、`xdotool`、`paplay` 同 `notify-send` 呢啲桌面工作階段工具。
- 內附例子預設係 X11 風格桌面工作階段，因為而家文字插入方式靠 `xdotool` 同 `xclip`。
- 視乎你用緊咩桌面環境，可能仲要俾使用者服務攞到 `DISPLAY`、`XAUTHORITY`、`DBUS_SESSION_BUS_ADDRESS` 或 `XDG_RUNTIME_DIR`。

## 倉庫結構

- `src/parrotkey/asr`：ASR 後端適配層
- `src/parrotkey/audio`：音訊收錄工具
- `src/parrotkey/hotkey`：熱鍵處理
- `src/parrotkey/inject`：文字注入後端
- `src/parrotkey/pipeline`：端到端語音輸入流程
- `examples`：服務同部署例子

## 開發說明

而家程式碼放喺 `src/parrotkey` 套件底下，第一版原型已經拆成設定、ASR 後端、文字注入同主流程模組。

## 路線圖

- 喺統一介面下接更多 ASR 後端
- 定義清晰嘅 ASR 後端介面
- 加入唔同文字注入方式嘅介面
- 加入設定同日誌能力
- 探索更快嘅本地後端同串流支援

## 授權

請睇 [LICENSE](LICENSE)。
