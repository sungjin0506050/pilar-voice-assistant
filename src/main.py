from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.brain import reply
from src.config import NAME_KO
from src.listen import record_seconds
from src.speak import speak
from src.transcribe import transcribe


def handle_text(text: str, speak_reply: bool, watch: bool = False) -> str:
    answer = reply(text, watch=watch)
    if not answer:
        print(f"(무시) {text}")
        return ""
    print(f"나: {text}")
    print(f"{NAME_KO}: {answer}")
    if speak_reply and answer != "종료":
        speak(answer, play=True)
    return answer


def watch_loop(speak_reply: bool) -> int:
    print(f"{NAME_KO}가 듣고 있습니다. 헤이 없이 {NAME_KO}만 부르세요. 종료라고 하면 끝납니다.")
    while True:
        try:
            wav = record_seconds(4)
            text = transcribe(wav)
        except RuntimeError as err:
            print(err)
            print("마이크를 못 찾으면 엔터 모드로 쓰세요: python -m src.main")
            return 1
        if not (text or "").strip():
            continue
        answer = handle_text(text, speak_reply=speak_reply, watch=True)
        if answer == "종료":
            return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="필라르")
    parser.add_argument("--speak", metavar="TEXT", help="문장을 읽어 줍니다")
    parser.add_argument("--file", metavar="WAV", help="wav 파일을 글자로 바꿉니다")
    parser.add_argument("--listen", type=int, metavar="SEC", help="마이크를 N초 녹음한 뒤 처리")
    parser.add_argument("--text", metavar="TEXT", help="음성 없이 글자로 시험")
    parser.add_argument("--watch", action="store_true", help="계속 들으며 필라르만 반응")
    parser.add_argument("--no-play", action="store_true", help="스피커 재생 생략")
    args = parser.parse_args()
    play = not args.no_play

    if args.speak:
        path = speak(args.speak, play=play)
        print(path)
        return 0

    if args.file:
        text = transcribe(Path(args.file))
        handle_text(text, speak_reply=play)
        return 0

    if args.text:
        handle_text(args.text, speak_reply=play)
        return 0

    if args.watch:
        return watch_loop(speak_reply=play)

    if args.listen:
        wav = record_seconds(args.listen)
        text = transcribe(wav)
        handle_text(text, speak_reply=play)
        return 0

    print(f"{NAME_KO}, 하고 이어서 말하면 됩니다. 헤이 없이. 종료라고 하면 끝납니다.")
    while True:
        input("준비되면 엔터 > ")
        wav = record_seconds(5)
        text = transcribe(wav)
        answer = handle_text(text, speak_reply=play)
        if answer == "종료":
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
