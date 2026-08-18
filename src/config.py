from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
TOOLS = ROOT / "tools"
MODELS = ROOT / "models"
RUNTIME = ROOT / "runtime"
VENV_PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"
ENV_PATH = ROOT / ".env"

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
CURSOR_MODEL = "composer-2.5"
DEFAULT_WORKSPACE = Path(r"D:\Projects\tjkimeye-staff")

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


def load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    if not ENV_PATH.exists():
        return values
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#") or "=" not in raw:
            continue
        key, _, value = raw.partition("=")
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def env(name: str, default: str = "") -> str:
    return (os.environ.get(name) or load_env().get(name) or default).strip()


def cursor_api_key() -> str:
    return env("CURSOR_API_KEY")


def workspace_path() -> Path:
    raw = env("PILAR_WORKSPACE")
    path = Path(raw) if raw else DEFAULT_WORKSPACE
    return path if path.exists() else ROOT


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
