from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.brain import reply
from src.speak import speak, wav_duration_sec
from src.transcribe import transcribe

PHRASE = "오늘은 날씨가 좋습니다"
MUST_HAVE = ("오늘", "날씨")


def main() -> int:
    errors: list[str] = []

    time_reply = reply("지금 몇 시야")
    if "시" not in time_reply:
        errors.append(f"시간 답변 실패: {time_reply}")

    named = reply("필라르 지금 몇 시야")
    if "시" not in named:
        errors.append(f"필라르 호출 뒤 시간 실패: {named}")

    who = reply("필라르")
    if "필라르" not in who:
        errors.append(f"이름 응답 실패: {who}")

    coding_reply = reply("이 버그 고쳐줘")
    if "Cursor" not in coding_reply and "코딩" not in coding_reply:
        errors.append(f"코딩 큐 실패: {coding_reply}")

    wav = speak(PHRASE, play=False)
    if wav_duration_sec(wav) < 0.8:
        errors.append(f"TTS wav 가 너무 짧음: {wav}")

    heard = transcribe(wav)
    print(f"말한 문장: {PHRASE}")
    print(f"알아들은 문장: {heard}")
    missing = [word for word in MUST_HAVE if word not in heard.replace(" ", "")]
    if missing:
        errors.append(f"STT 가 핵심 단어를 못 찾음 {missing}: {heard}")

    if errors:
        print("VERIFY FAIL")
        for item in errors:
            print("-", item)
        return 1

    print("VERIFY PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
