from __future__ import annotations

from datetime import datetime

from src.config import CURSOR_MODEL, RUNTIME, cursor_api_key, workspace_path

CURSOR_QUEUE = RUNTIME / "cursor-queue.txt"

CODING_WORDS = (
    "코딩",
    "고쳐",
    "만들어",
    "커밋",
    "리팩터",
    "테스트",
    "버그",
    "수정",
    "작성",
    "구현",
)


def is_coding(text: str) -> bool:
    return any(word in text for word in CODING_WORDS)


def _queue(prompt: str) -> None:
    CURSOR_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    with CURSOR_QUEUE.open("a", encoding="utf-8") as handle:
        handle.write(f"{datetime.now().isoformat(timespec='seconds')} {prompt}\n")


def _spoken(text: str) -> str:
    compact = " ".join((text or "").split())
    if not compact:
        return "코딩 끝냈어요."
    if len(compact) <= 180:
        return compact
    return compact[:180].rstrip() + "."


def send_coding(prompt: str) -> str:
    """말로 시킨 코딩을 Cursor 로컬 에이전트에 넘깁니다. 키 없으면 적어 둡니다."""
    _queue(prompt)
    key = cursor_api_key()
    if not key:
        return (
            "코딩 요청은 적어 두었어요. Cursor 키가 아직 없어요. "
            ".env 파일에 CURSOR_API_KEY 를 넣으면 바로 실행합니다."
        )

    cwd = workspace_path()
    print(f"Cursor에 넘김: {cwd}")
    try:
        from cursor_sdk import Agent, AgentOptions, CursorAgentError, LocalAgentOptions
    except ImportError:
        return "Cursor 도구가 없어요. 적어 두었어요."

    instruction = (
        "사용자가 말로 시킨 일입니다. 해당 작업만 하세요. "
        "끝나면 한국어로 두 문장 안에 무엇을 했는지 말하세요.\n\n"
        f"{prompt}"
    )
    try:
        result = Agent.prompt(
            instruction,
            AgentOptions(
                api_key=key,
                model=CURSOR_MODEL,
                name="Pilar",
                local=LocalAgentOptions(cwd=str(cwd)),
            ),
        )
    except CursorAgentError as err:
        return f"Cursor에 연결하지 못했어요. 적어 두었어요. {err}"
    except Exception as err:  # noqa: BLE001
        return f"코딩을 시작하지 못했어요. 적어 두었어요. {err}"

    if str(result.status).lower() in {"error", "failed", "cancelled"}:
        return "코딩 중에 막혔어요. 적어 두었어요."
    return _spoken(result.result)
