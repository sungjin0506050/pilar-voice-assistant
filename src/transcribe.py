from __future__ import annotations

import subprocess
from pathlib import Path

from src.config import RUNTIME, find_whisper_cli, model_path


def transcribe(wav_path: Path, language: str = "ko") -> str:
    """16kHz wav 파일을 한국어 글자로 바꿉니다."""
    wav_path = Path(wav_path)
    if not wav_path.exists():
        raise FileNotFoundError(wav_path)

    out_txt = RUNTIME / f"{wav_path.stem}.txt"
    cmd = [
        str(find_whisper_cli()),
        "-m",
        str(model_path()),
        "-f",
        str(wav_path),
        "-l",
        language,
        "-otxt",
        "-of",
        str(RUNTIME / wav_path.stem),
        "-np",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "whisper 실행 실패")
    if not out_txt.exists():
        raise RuntimeError("whisper 가 텍스트 파일을 만들지 않았습니다.")
    return out_txt.read_text(encoding="utf-8").strip()
