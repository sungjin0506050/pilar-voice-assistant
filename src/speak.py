from __future__ import annotations

import asyncio
import subprocess
import uuid
import wave
import winsound
from pathlib import Path

import edge_tts
import imageio_ffmpeg

from src.config import RUNTIME, SAMPLE_RATE, TTS_VOICE


def ffmpeg_bin() -> str:
    return imageio_ffmpeg.get_ffmpeg_exe()


async def _synthesize(text: str, mp3_path: Path, voice: str) -> None:
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(mp3_path))


def mp3_to_wav(mp3_path: Path, wav_path: Path) -> None:
    cmd = [
        ffmpeg_bin(),
        "-y",
        "-i",
        str(mp3_path),
        "-ac",
        "1",
        "-ar",
        str(SAMPLE_RATE),
        str(wav_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def speak(text: str, play: bool = True, voice: str = TTS_VOICE) -> Path:
    """한국어 문장을 읽어 16kHz wav 를 만들고, 필요하면 스피커로 재생합니다."""
    text = (text or "").strip()
    if not text:
        raise ValueError("읽을 문장이 비어 있습니다.")

    stem = uuid.uuid4().hex[:12]
    mp3_path = RUNTIME / f"{stem}.mp3"
    wav_path = RUNTIME / f"{stem}.wav"
    asyncio.run(_synthesize(text, mp3_path, voice))
    mp3_to_wav(mp3_path, wav_path)
    mp3_path.unlink(missing_ok=True)

    if play:
        winsound.PlaySound(str(wav_path), winsound.SND_FILENAME)
    return wav_path


def wav_duration_sec(wav_path: Path) -> float:
    with wave.open(str(wav_path), "rb") as handle:
        return handle.getnframes() / float(handle.getframerate())
