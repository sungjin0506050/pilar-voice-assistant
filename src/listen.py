from __future__ import annotations

import subprocess
from pathlib import Path

from src.config import RUNTIME, SAMPLE_RATE
from src.speak import ffmpeg_bin


def list_dshow_audio_devices() -> str:
    cmd = [ffmpeg_bin(), "-list_devices", "true", "-f", "dshow", "-i", "dummy"]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (result.stderr or "") + (result.stdout or "")


def record_seconds(seconds: int = 5, wav_path: Path | None = None) -> Path:
    """내장/기본 마이크로 seconds 초 녹음합니다. 마이크가 없으면 에러를 냅니다."""
    wav_path = wav_path or (RUNTIME / "last-listen.wav")
    cmd = [
        ffmpeg_bin(),
        "-y",
        "-f",
        "dshow",
        "-i",
        "audio=default",
        "-t",
        str(seconds),
        "-ac",
        "1",
        "-ar",
        str(SAMPLE_RATE),
        str(wav_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0 or not wav_path.exists():
        raise RuntimeError(
            "마이크 녹음에 실패했습니다. 새 노트북에서 마이크 허용 후 다시 시도하세요.\n"
            + (result.stderr or result.stdout or "")
        )
    return wav_path
