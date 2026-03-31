# ParrotKey

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [粵語](README.yue.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

ParrotKey는 로컬에서 동작하는 푸시투토크 음성 입력 프레임워크입니다.

키를 누른 채 말하고, 키를 떼면 텍스트가 나타납니다.

## 무엇을 할 수 있나

- 핫키를 누르고 있는 동안 마이크 입력을 캡처합니다
- 키를 놓는 순간 음성 인식을 실행합니다
- 인식된 텍스트를 현재 활성화된 애플리케이션에 삽입합니다
- ASR 백엔드와 텍스트 입력 방식을 확장하기 쉬운 구조를 유지합니다

## 현재 상태

첫 번째 프로토타입이 이미 포함되어 있습니다.

현재는 Linux 데스크톱 워크플로를 중심으로 다음 기능을 제공합니다.

- `Right Ctrl` 푸시투토크
- PyTorch 기반 CPU 로컬 `Qwen3-ASR`
- 클립보드 기반 활성 창 붙여넣기
- 선택 가능한 비프음과 데스크톱 알림

## 프로젝트 목표

- 로컬에서 실행하여 음성 데이터를 사용자의 머신 안에 유지하기
- 데스크톱 환경에서 푸시투토크 음성 입력 지원하기
- ASR 백엔드에 종속되지 않는 구조로 여러 모델을 쉽게 연결하기
- 붙여넣기, 키 입력 에뮬레이션, IME 연동 등 유연한 텍스트 삽입 방식 제공하기
- 로컬 LLM 후처리를 위한 확장 지점 남겨두기

## 계획 중인 아키텍처

- `parrotkey.audio`: 마이크 캡처와 버퍼링
- `parrotkey.hotkey`: 전역 핫키 처리
- `parrotkey.asr`: ASR 백엔드 어댑터
- `parrotkey.inject`: 텍스트 삽입 백엔드
- `parrotkey.pipeline`: 엔드 투 엔드 음성 입력 파이프라인

## 초기 범위

- Linux 데스크톱 중심
- 푸시투토크 상호작용
- 로컬 ASR 백엔드 지원
- 클립보드 붙여넣기 또는 입력 에뮬레이션

## 빠른 시작

현재 실행 가능한 프로토타입은 기존 로컬 입력 스크립트의 흐름을 따릅니다.

- `Right Ctrl` 을 눌러 녹음 시작
- 키를 떼면 인식 실행
- 인식된 텍스트를 현재 활성 창에 붙여넣기
- CPU + PyTorch 기반 Qwen3-ASR 사용

가상 환경을 만들고 활성화합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

패키지를 설치합니다.

```bash
pip install -e .
pip install -r requirements.txt
```

ParrotKey를 실행합니다.

```bash
parrotkey --model-path /path/to/Qwen3-ASR-0.6B
```

설치 없이 실행하려면:

```bash
PYTHONPATH=src python3 -m parrotkey --model-path /path/to/Qwen3-ASR-0.6B
```

현재 Linux 프로토타입에서 필요한 시스템 도구:

- `xclip`
- `xdotool`
- `paplay`
- `notify-send`

## 모델

현재 프로토타입은 `Qwen3-ASR-0.6B` 의 로컬 사본을 필요로 합니다.

공식 Hugging Face 페이지:

https://huggingface.co/Qwen/Qwen3-ASR-0.6B

다운로드 예시:

```bash
huggingface-cli download Qwen/Qwen3-ASR-0.6B --local-dir /path/to/Qwen3-ASR-0.6B
```

## 사용자 서비스로 실행하기

로그인 후에도 ParrotKey를 계속 사용할 수 있게 하려면 `systemd --user` 서비스로 실행하는 것이 좋습니다.

예시 unit 파일은 `examples/parrotkey.service` 에 포함되어 있습니다.

1. 사용자 서비스 디렉터리를 만듭니다.

```bash
mkdir -p ~/.config/systemd/user
```

2. 예시 서비스 파일을 복사합니다.

```bash
cp examples/parrotkey.service ~/.config/systemd/user/parrotkey.service
```

3. 서비스 파일에서 다음 항목을 수정합니다.

- `WorkingDirectory`
- `Environment=PATH=...`
- `ExecStart`
- `--model-path`

4. 다시 불러오고 시작합니다.

```bash
systemctl --user daemon-reload
systemctl --user enable --now parrotkey.service
```

5. 필요하면 로그를 확인합니다.

```bash
journalctl --user -u parrotkey.service -f
```

주의:

- 현재 프로토타입은 `xclip`, `xdotool`, `paplay`, `notify-send` 같은 데스크톱 세션 도구에 의존합니다.
- 포함된 예시는 현재 텍스트 삽입이 `xdotool` 과 `xclip` 에 의존하기 때문에 X11 스타일 데스크톱 세션을 가정합니다.
- 데스크톱 환경에 따라 `DISPLAY`, `XAUTHORITY`, `DBUS_SESSION_BUS_ADDRESS`, `XDG_RUNTIME_DIR` 를 사용자 서비스 환경에 전달해야 할 수 있습니다.

## 개발

현재 코드베이스는 `src/parrotkey` 패키지 아래에 있으며, 첫 번째 프로토타입은 설정, ASR 백엔드, 텍스트 삽입, 파이프라인 모듈로 나뉘어 있습니다.

## 문서 관리

이 저장소는 여러 언어의 README를 함께 관리합니다.

앞으로 README 내용을 수정하거나 새 README 섹션을 추가할 때는 다음 파일들도 함께 업데이트해 주세요.

- `README.md`
- `README.zh-CN.md`
- `README.zh-TW.md`
- `README.yue.md`
- `README.ja.md`
- `README.ko.md`

## 로드맵

- 공통 인터페이스 아래에서 더 많은 ASR 백엔드 추가
- 명확한 ASR 백엔드 인터페이스 정의
- 다양한 텍스트 삽입 방식용 인터페이스 추가
- 설정과 로깅 기능 추가
- 더 빠른 로컬 백엔드와 스트리밍 지원 탐색

## 라이선스

[LICENSE](LICENSE)를 참고하세요.
