# ParrotKey

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [粵語](README.yue.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform: Linux](https://img.shields.io/badge/platform-Linux-blue.svg)](README.md)
[![Prototype](https://img.shields.io/badge/status-prototype-orange.svg)](README.md)
[![Hugging Face Qwen3-ASR-0.6B](https://img.shields.io/badge/model-Qwen3--ASR--0.6B-yellow.svg)](https://huggingface.co/Qwen/Qwen3-ASR-0.6B)

ParrotKey 是一个本地的按键通话式语音输入框架。

按住一个键，说话，松开，文字就会出现。

ParrotKey 的目标是成为一个与后端无关的本地语音输入基础框架，而当前第一版从基于 Qwen3-ASR 的 Linux 原型开始。

## 目录

- [它能做什么](#它能做什么)
- [当前状态](#当前状态)
- [快速开始](#快速开始)
- [模型](#模型)
- [作为用户服务运行](#作为用户服务运行)
- [仓库结构](#仓库结构)
- [路线图](#路线图)

## 它能做什么

- 在按住热键时采集麦克风音频
- 在松开按键后运行语音识别
- 将识别出的文字插入当前活动应用
- 保持后端和文本注入方式可扩展

## 当前状态

第一个原型已经包含在仓库中。

目前它主要面向 Linux 桌面工作流，支持：

- 按住 `Right Ctrl` 讲话
- 通过 PyTorch 在 CPU 上运行本地 `Qwen3-ASR`
- 通过剪贴板粘贴到当前窗口
- 可选提示音和桌面通知

## 项目目标

- 本地运行，让语音数据留在你的机器上
- 支持桌面系统上的按键通话式语音输入
- 保持 ASR 后端无关，方便接入不同模型
- 让文本注入方式更灵活，例如粘贴、模拟键入、IME 集成
- 为本地 LLM 后处理留出空间

## 规划中的架构

- `parrotkey.audio`：麦克风采集与缓冲
- `parrotkey.hotkey`：全局热键处理
- `parrotkey.asr`：ASR 后端适配层
- `parrotkey.inject`：文本注入后端
- `parrotkey.pipeline`：端到端语音输入流程

## 初始范围

- 以 Linux 桌面为主
- 按键通话交互
- 本地 ASR 后端支持
- 剪贴板粘贴或模拟输入输出

## 快速开始

当前可运行原型延续了原来的本地输入脚本：

- 按住 `Right Ctrl` 开始录音
- 松开后进行识别
- 将识别文本粘贴到当前活动窗口
- 使用基于 CPU + PyTorch 的 Qwen3-ASR

创建并激活虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

安装项目：

```bash
pip install -e .
pip install -r requirements.txt
```

运行 ParrotKey：

```bash
parrotkey --model-path /path/to/Qwen3-ASR-0.6B
```

如果不安装，也可以这样运行：

```bash
PYTHONPATH=src python3 -m parrotkey --model-path /path/to/Qwen3-ASR-0.6B
```

当前 Linux 需要的系统工具：

- `xclip`
- `xdotool`
- `paplay`
- `notify-send`

## 模型

当前原型需要本地准备一份 `Qwen3-ASR-0.6B`。

官方 Hugging Face 页面：

https://huggingface.co/Qwen/Qwen3-ASR-0.6B

下载示例：

```bash
huggingface-cli download Qwen/Qwen3-ASR-0.6B --local-dir /path/to/Qwen3-ASR-0.6B
```

## 作为用户服务运行

如果你希望 ParrotKey 在登录后常驻运行，推荐使用 `systemd --user` 服务。

示例 unit 文件位于 `examples/parrotkey.service`。

1. 创建用户服务目录：

```bash
mkdir -p ~/.config/systemd/user
```

2. 复制示例服务文件：

```bash
cp examples/parrotkey.service ~/.config/systemd/user/parrotkey.service
```

3. 编辑服务文件，并修改这些项：

- `WorkingDirectory`
- `Environment=PATH=...`
- `ExecStart`
- `--model-path`

4. 重新加载并启动服务：

```bash
systemctl --user daemon-reload
systemctl --user enable --now parrotkey.service
```

5. 如果需要查看日志：

```bash
journalctl --user -u parrotkey.service -f
```

注意：

- 当前原型依赖 `xclip`、`xdotool`、`paplay` 和 `notify-send` 这类桌面会话工具。
- 示例服务默认按 X11 风格桌面会话来写，因为当前文本插入方式基于 `xdotool` 和 `xclip`。
- 具体桌面环境下，可能还需要让用户服务继承 `DISPLAY`、`XAUTHORITY`、`DBUS_SESSION_BUS_ADDRESS` 或 `XDG_RUNTIME_DIR`。

## 仓库结构

- `src/parrotkey/asr`：ASR 后端适配层
- `src/parrotkey/audio`：音频采集工具
- `src/parrotkey/hotkey`：热键处理
- `src/parrotkey/inject`：文本注入后端
- `src/parrotkey/pipeline`：端到端语音输入流程
- `examples`：服务与部署示例

## 开发说明

当前代码位于 `src/parrotkey` 包下，第一版原型已经拆分为配置、ASR 后端、文本注入和主流程模块。

## 路线图

- 在统一接口下接入更多 ASR 后端
- 定义清晰的 ASR 后端接口
- 增加不同文本注入方式的接口
- 增加配置和日志能力
- 探索更快的本地后端和流式支持

## 许可证

见 [LICENSE](LICENSE)。
