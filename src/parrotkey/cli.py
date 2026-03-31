import argparse

from parrotkey.config import AppConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="parrotkey",
        description="Local push-to-talk voice typing with pluggable ASR backends.",
    )
    parser.add_argument(
        "--model-path",
        required=True,
        help="Path to the local Qwen3-ASR model directory.",
    )
    parser.add_argument(
        "--input-device",
        default="pulse",
        help="sounddevice input device name or index.",
    )
    parser.add_argument(
        "--input-channels",
        type=int,
        default=4,
        help="Number of input channels to capture.",
    )
    parser.add_argument(
        "--language",
        default="Chinese",
        help="ASR language hint. Use 'None' to enable auto-detect.",
    )
    parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=96,
        help="Maximum decode length for the ASR model.",
    )
    parser.add_argument(
        "--save-debug-wav",
        action="store_true",
        help="Save recorded audio to debug_record.wav before transcription.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    language = None if args.language == "None" else args.language
    config = AppConfig(
        model_path=args.model_path,
        input_device=args.input_device,
        input_channels=args.input_channels,
        language=language,
        max_new_tokens=args.max_new_tokens,
        save_debug_wav=args.save_debug_wav,
    )
    from parrotkey.pipeline.push_to_talk import run_push_to_talk_app

    run_push_to_talk_app(config)
    return 0
