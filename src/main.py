from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.brain import reply
from src.listen import record_seconds
from src.speak import speak
from src.transcribe import transcribe


def handle_text(text: str, speak_reply: bool) -> str:
    answer = reply(text)
    print(f"나: {text}")
    print(f"비서: {answer}")
    if speak_reply and answer != "종료":
        speak(answer, play=True)
    return answer


def main() -> int:
    parser = argparse.ArgumentParser(description="로컬 음성 비서")
    parser.add_argument("--speak", metavar="TEXT", help="문장을 읽어 줍니다")
    parser.add_argument("--file", metavar="WAV", help="wav 파일을 글자로 바꿉니다")
    parser.add_argument("--listen", type=int, metavar="SEC", help="마이크를 N초 녹음한 뒤 처리")
    parser.add_argument("--text", metavar="TEXT", help="음성 없이 글자로 시험")
    parser.add_argument("--no-play", action="store_true", help="스피커 재생 생략")
    args = parser.parse_args()

    if args.speak:
        path = speak(args.speak, play=not args.no_play)
        print(path)
        return 0

    if args.file:
        text = transcribe(Path(args.file))
        handle_text(text, speak_reply=not args.no_play)
        return 0

    if args.text:
        handle_text(args.text, speak_reply=not args.no_play)
        return 0

    if args.listen:
        wav = record_seconds(args.listen)
        text = transcribe(wav)
        handle_text(text, speak_reply=not args.no_play)
        return 0

    print("필라르, 하고 이어서 말하면 됩니다. 헤이 없이. 종료라고 하면 끝납니다.")
    while True:
        input("준비되면 엔터 > ")
        wav = record_seconds(5)
        text = transcribe(wav)
        answer = handle_text(text, speak_reply=not args.no_play)
        if answer == "종료":
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
