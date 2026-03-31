# ParrotKey

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [粵語](README.yue.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform: Linux](https://img.shields.io/badge/platform-Linux-blue.svg)](README.md)
[![Prototype](https://img.shields.io/badge/status-prototype-orange.svg)](README.md)
[![Hugging Face Qwen3-ASR-0.6B](https://img.shields.io/badge/model-Qwen3--ASR--0.6B-yellow.svg)](https://huggingface.co/Qwen/Qwen3-ASR-0.6B)

ParrotKey はローカルで動作するプッシュツートーク型の音声入力フレームワークです。

キーを押しながら話し、離すと文字が現れます。

ParrotKey はバックエンド非依存のローカル音声入力基盤を目指しており、現在の第一歩として Qwen3-ASR ベースの Linux プロトタイプから始めています。

## 目次

- [できること](#できること)
- [現在の状態](#現在の状態)
- [クイックスタート](#クイックスタート)
- [モデル](#モデル)
- [ユーザーサービスとして実行する](#ユーザーサービスとして実行する)
- [リポジトリ構成](#リポジトリ構成)
- [ロードマップ](#ロードマップ)

## できること

- ホットキーを押している間だけマイク入力を取得する
- キーを離したタイミングで音声認識を実行する
- 認識された文字を現在アクティブなアプリに挿入する
- ASR バックエンドや文字入力方式を拡張しやすい構成を保つ

## 現在の状態

最初のプロトタイプがすでに含まれています。

現時点では Linux デスクトップ向けで、次の機能を持っています。

- `Right Ctrl` によるプッシュツートーク
- PyTorch を使った CPU 上のローカル `Qwen3-ASR`
- クリップボード経由でアクティブウィンドウへ貼り付け
- 任意の効果音とデスクトップ通知

## プロジェクトの目標

- ローカル実行で音声データを自分のマシン内にとどめる
- デスクトップ環境向けのプッシュツートーク音声入力を提供する
- ASR バックエンド非依存の設計で、さまざまなモデルを接続しやすくする
- 貼り付け、疑似キーボード入力、IME 連携など柔軟な文字注入方式を用意する
- ローカル LLM による後処理を追加しやすくする

## 予定しているアーキテクチャ

- `parrotkey.audio`: マイク入力とバッファリング
- `parrotkey.hotkey`: グローバルホットキー処理
- `parrotkey.asr`: ASR バックエンドアダプタ
- `parrotkey.inject`: 文字注入バックエンド
- `parrotkey.pipeline`: 音声入力のエンドツーエンド処理

## 初期スコープ

- Linux デスクトップを中心にする
- プッシュツートーク操作
- ローカル ASR バックエンド対応
- クリップボード貼り付けまたは疑似入力

## クイックスタート

現在動作するプロトタイプは、元のローカル入力スクリプトを引き継いでいます。

- `Right Ctrl` を押して録音開始
- 離すと認識を実行
- 認識結果をアクティブウィンドウに貼り付け
- CPU + PyTorch 版の Qwen3-ASR を使用

仮想環境を作成して有効化します。

```bash
python3 -m venv .venv
source .venv/bin/activate
```

パッケージをインストールします。

```bash
pip install -e .
pip install -r requirements.txt
```

ParrotKey を実行します。

```bash
parrotkey --model-path /path/to/Qwen3-ASR-0.6B
```

インストールせずに実行する場合：

```bash
PYTHONPATH=src python3 -m parrotkey --model-path /path/to/Qwen3-ASR-0.6B
```

現在の Linux プロトタイプで必要なシステムツール：

- `xclip`
- `xdotool`
- `paplay`
- `notify-send`

## モデル

現在のプロトタイプでは `Qwen3-ASR-0.6B` をローカルに用意する必要があります。

公式 Hugging Face ページ：

https://huggingface.co/Qwen/Qwen3-ASR-0.6B

ダウンロード例：

```bash
huggingface-cli download Qwen/Qwen3-ASR-0.6B --local-dir /path/to/Qwen3-ASR-0.6B
```

## ユーザーサービスとして実行する

ログイン後も ParrotKey を常駐させたい場合は、`systemd --user` サービスとして動かすのがおすすめです。

サンプルの unit ファイルは `examples/parrotkey.service` にあります。

1. ユーザーサービス用ディレクトリを作成します。

```bash
mkdir -p ~/.config/systemd/user
```

2. サンプルのサービスファイルをコピーします。

```bash
cp examples/parrotkey.service ~/.config/systemd/user/parrotkey.service
```

3. サービスファイルを編集し、次の項目を更新します。

- `WorkingDirectory`
- `Environment=PATH=...`
- `ExecStart`
- `--model-path`

4. 再読み込みして起動します。

```bash
systemctl --user daemon-reload
systemctl --user enable --now parrotkey.service
```

5. 必要ならログを確認します。

```bash
journalctl --user -u parrotkey.service -f
```

注意：

- 現在のプロトタイプは `xclip`、`xdotool`、`paplay`、`notify-send` のようなデスクトップセッション用ツールに依存しています。
- 同梱のサンプルは X11 系のデスクトップ環境を前提にしています。現在の文字注入は `xdotool` と `xclip` を使うためです。
- デスクトップ環境によっては、`DISPLAY`、`XAUTHORITY`、`DBUS_SESSION_BUS_ADDRESS`、`XDG_RUNTIME_DIR` をユーザーサービス側に渡す必要があります。

## リポジトリ構成

- `src/parrotkey/asr`: ASR バックエンドアダプタ
- `src/parrotkey/audio`: 音声入力ユーティリティ
- `src/parrotkey/hotkey`: ホットキー処理
- `src/parrotkey/inject`: 文字注入バックエンド
- `src/parrotkey/pipeline`: エンドツーエンドの音声入力フロー
- `examples`: サービスとデプロイ例

## 開発

現在のコードベースは `src/parrotkey` パッケージ以下にあり、最初のプロトタイプは設定、ASR バックエンド、文字注入、パイプラインに分割されています。

## ロードマップ

- 共通インターフェースのもとで ASR バックエンドを追加する
- 明確な ASR バックエンドインターフェースを定義する
- さまざまな文字注入方式のインターフェースを追加する
- 設定とログ機能を追加する
- より高速なローカルバックエンドとストリーミング対応を探る

## ライセンス

[LICENSE](LICENSE) を参照してください。
