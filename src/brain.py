from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.config import NAME_KO, RUNTIME, WAKE_ALIASES

NOTES = RUNTIME / "notes.txt"
CURSOR_QUEUE = RUNTIME / "cursor-queue.txt"


def strip_wake(text: str) -> tuple[str, bool]:
    """앞의 필라르를 떼고, 불렀는지만 돌려줍니다. Hey 는 쓰지 않습니다."""
    raw = (text or "").strip()
    if not raw:
        return "", False
    compact = raw.replace(" ", "")
    lowered = compact.casefold()
    for wake in WAKE_ALIASES:
        token = wake.replace(" ", "")
        if lowered == token.casefold():
            return "", True
        prefix = token.casefold()
        if lowered.startswith(prefix):
            rest = compact[len(token) :]
            rest = rest.lstrip(" ,야아,.?")
            return rest.strip(), True
    return raw, False


def reply(user_text: str) -> str:
    """말한 문장을 받아 짧은 한국어 답을 만듭니다. Cursor 연결은 다음 단계."""
    text, called = strip_wake(user_text)
    if not text:
        if called:
            return f"듣고 있어요. {NAME_KO}입니다."
        return "잘 못 들었어요. 다시 말해 주세요."

    lower = text.replace(" ", "")

    if any(word in lower for word in ("누구", "이름", "너뭐야", "자기소개")):
        return f"{NAME_KO}입니다. 기둥이에요."

    if any(word in lower for word in ("종료", "그만", "꺼져", "안녕그만")):
        return "종료"

    if "몇시" in lower or "지금시간" in lower or "몇시야" in lower:
        now = datetime.now().strftime("%p %I시 %M분").replace("AM", "오전").replace("PM", "오후")
        return f"지금 {now}이에요."

    if "날짜" in lower or "오늘며칠" in lower:
        return datetime.now().strftime("오늘은 %Y년 %m월 %d일이에요.")

    if text.startswith("메모") or text.startswith("메모해"):
        note = text.split(" ", 1)[1].strip() if " " in text else text
        NOTES.parent.mkdir(parents=True, exist_ok=True)
        with NOTES.open("a", encoding="utf-8") as handle:
            handle.write(f"{datetime.now().isoformat(timespec='seconds')} {note}\n")
        return "메모해 두었어요."

    if any(word in text for word in ("코딩", "고쳐", "만들어", "커밋", "배포")):
        CURSOR_QUEUE.parent.mkdir(parents=True, exist_ok=True)
        with CURSOR_QUEUE.open("a", encoding="utf-8") as handle:
            handle.write(f"{datetime.now().isoformat(timespec='seconds')} {text}\n")
        return "코딩 요청은 적어 두었어요. Cursor 연결은 다음 단계에서 붙입니다."

    return f"들었어요. {text}"
