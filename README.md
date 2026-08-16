# 필라르 (Pilar)

스페인어로 기둥. 부를 때는 **헤이 없이** `필라르`만 말합니다.

새 레노버 노트북으로 **폴더 통째 복사**하면 됩니다. 병원 직원 포털과는 다른 프로젝트입니다.

위치: `D:\Projects\voice-assistant`

## 이 PC에서 이미 된 것

- 말하면 글자로 바꾸는 뼈대 (whisper.cpp)
- 글자를 한국어로 읽어 주는 뼈대 (edge-tts)
- 시간 / 메모 / 코딩 요청 적어두기
- `scripts/verify.py` 로 말→글자 왕복 검사

아직 안 된 것: Cursor에 직접 코딩 시키기, 항상 대기하며 필라르만 듣기.

## 새 노트북에서

1. 이 폴더를 D드라이브에 복사
2. PowerShell에서:

```powershell
cd D:\Projects\voice-assistant
.\scripts\setup.ps1
.\.venv\Scripts\python.exe scripts\verify.py
```

3. 마이크로 쓰려면:

```powershell
.\.venv\Scripts\python.exe -m src.main --listen 5
```

엔터 누른 뒤 말하기:

```powershell
.\.venv\Scripts\python.exe -m src.main
```
