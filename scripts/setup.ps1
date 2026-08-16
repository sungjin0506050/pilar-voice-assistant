$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$env:TEMP = Join-Path $Root ".cache\tmp"
$env:TMP = $env:TEMP
$env:PIP_CACHE_DIR = Join-Path $Root ".cache\pip"
New-Item -ItemType Directory -Force -Path $env:TEMP, $env:PIP_CACHE_DIR, (Join-Path $Root "tools"), (Join-Path $Root "models") | Out-Null

$Python = "python"
& $Python -m venv (Join-Path $Root ".venv")
$VenvPy = Join-Path $Root ".venv\Scripts\python.exe"
& $VenvPy -m pip install --upgrade pip
& $VenvPy -m pip install -r (Join-Path $Root "requirements.txt")

$Zip = Join-Path $Root "tools\whisper-bin-x64.zip"
$WhisperUrl = "https://github.com/ggml-org/whisper.cpp/releases/download/v1.9.2/whisper-bin-x64.zip"
if (-not (Get-ChildItem -Path (Join-Path $Root "tools") -Recurse -Filter "whisper-cli.exe" -ErrorAction SilentlyContinue)) {
    Write-Host "Downloading whisper.cpp..."
    Invoke-WebRequest -Uri $WhisperUrl -OutFile $Zip
    Expand-Archive -Path $Zip -DestinationPath (Join-Path $Root "tools\whisper") -Force
}

$Model = Join-Path $Root "models\ggml-small-q5_1.bin"
$ModelUrl = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small-q5_1.bin"
if (-not (Test-Path $Model)) {
    Write-Host "Downloading whisper model..."
    Invoke-WebRequest -Uri $ModelUrl -OutFile $Model
}

Write-Host "SETUP DONE"
& $VenvPy -c "import edge_tts, imageio_ffmpeg; print('python-ok', imageio_ffmpeg.get_ffmpeg_exe())"
Get-ChildItem -Path (Join-Path $Root "tools") -Recurse -Filter "whisper-cli.exe" | Select-Object -ExpandProperty FullName
Write-Host "model:" (Test-Path $Model) (if (Test-Path $Model) { (Get-Item $Model).Length })
