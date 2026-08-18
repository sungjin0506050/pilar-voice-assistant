# 필라르 (Pilar)

말로 Cursor를 시키는 개인 음성 비서입니다. 스페인어로 기둥. 부를 때는 **헤이 없이** `필라르`만 말합니다.

병원 직원 포털(`tjkimeye-staff`)과는 **다른 프로젝트**입니다.

## 새 노트북에서 (이 순서)

1. [Git](https://git-scm.com/download/win), [Python](https://www.python.org/downloads/), [Cursor](https://cursor.com) 설치
2. PowerShell:

```powershell
cd D:\Projects
git clone https://github.com/sungjin0506050/pilar-voice-assistant.git
cd pilar-voice-assistant
.\scripts\setup.ps1
.\.venv\Scripts\python.exe scripts\verify.py
.\.venv\Scripts\python.exe scripts\paste-key.py
```

`paste-key.py` 창에 Cursor 키를 붙여 넣고 저장하면 됩니다. 키 발급: https://cursor.com/dashboard/api

코딩할 폴더 기본값은 `D:\Projects\tjkimeye-staff` 입니다. 병원 포털도 노트북에 받아 두세요.

3. 필라르 켜기:

```powershell
.\.venv\Scripts\python.exe -m src.main --watch
```

`필라르, 이 버그 고쳐` 처럼 말하면 됩니다.

## 된 것

- 한국어 듣기 / 말하기
- `필라르`라고 불러야 반응
- 삭제·배포는 먼저 확인
- 코딩 말은 Cursor로 넘김 (키 있으면 실행)

## 올리지 않는 것

- `.env` (Cursor 키)
- 음성 모델, 가상환경 (노트북에서 `setup.ps1`이 다시 받음)
