from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
TOOLS = ROOT / "tools"
MODELS = ROOT / "models"
RUNTIME = ROOT / "runtime"
VENV_PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"

WHISPER_RELEASE = "v1.9.2"
WHISPER_ZIP_URL = (
    f"https://github.com/ggml-org/whisper.cpp/releases/download/"
    f"{WHISPER_RELEASE}/whisper-bin-x64.zip"
)
WHISPER_MODEL_URL = (
    "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small-q5_1.bin"
)
WHISPER_MODEL_NAME = "ggml-small-q5_1.bin"
TTS_VOICE = "ko-KR-SunHiNeural"
SAMPLE_RATE = 16000

# Call name only. No "Hey". Spanish: pillar.
NAME = "Pilar"
NAME_KO = "필라르"
WAKE_ALIASES = (
    "필라르",
    "필랄",
    "피라르",
    "pilar",
    "pillar",
)

for folder in (CACHE, TOOLS, MODELS, RUNTIME):
    folder.mkdir(parents=True, exist_ok=True)


def find_whisper_cli() -> Path:
    matches = list(TOOLS.rglob("whisper-cli.exe"))
    if not matches:
        matches = list(TOOLS.rglob("main.exe"))
    if not matches:
        raise FileNotFoundError("whisper-cli.exe 가 없습니다. scripts/setup.ps1 을 먼저 실행하세요.")
    return matches[0]


def model_path() -> Path:
    path = MODELS / WHISPER_MODEL_NAME
    if not path.exists():
        raise FileNotFoundError(f"모델이 없습니다: {path}")
    return path
