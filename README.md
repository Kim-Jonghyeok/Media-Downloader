# Media Downloader

Python으로 개발된 GUI 기반 미디어 다운로드 프로그램입니다. 이 프로그램은 교육 목적으로 제작되었으며, Python, tkinter, 그리고 미디어 처리 라이브러리의 학습을 위한 예제입니다.

## 주요 기능

- GUI 인터페이스로 쉬운 사용
- 다양한 해상도 옵션 지원 (4K/2160p ~ 360p)
- 실시간 다운로드 진행률 표시
- 저장 경로 선택 기능
- 안정적인 다운로드 (자동 재시도 기능)

## 시스템 요구사항

- Python 3.7 이상
- ffmpeg 설치 필요
- 인터넷 연결
- Windows/Linux/MacOS 지원

## 설치 방법

1. Python 설치 확인:
```bash
python --version
```

2. ffmpeg 설치:
- Windows: [ffmpeg 다운로드](https://ffmpeg.org/download.html)
- Linux: ```bash
sudo apt-get install ffmpeg```
- Mac: ```bash
brew install ffmpeg```

3. 필요한 패키지 설치:
```bash
python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

## 사용 방법

1. 프로그램 실행:
```bash
python media_downloader.py
```

2. URL 입력
3. 저장 경로 선택
4. 화질 선택
5. 다운로드 버튼 클릭

## 주의사항

- 이 프로그램은 교육 및 학습 목적으로 제작되었습니다
- 저작권이 있는 콘텐츠는 저작권자의 허가를 받고 사용하세요
- 불법적인 목적으로의 사용을 금지합니다
- 개인적인 학습 용도로만 사용해주세요

## 개발자 정보

- 이슈 리포트나 기능 제안은 GitHub Issues를 통해 제출해주세요
- 프로그램 개선 및 버그 수정에 참여하실 수 있습니다

## 라이선스

MIT License

## 기여하기

1. 이 저장소를 Fork 하세요
2. 새로운 Branch를 만드세요
3. 수정사항을 Commit 하세요
4. Branch에 Push 하세요
5. Pull Request를 보내주세요

## 교육용 참고 자료

이 프로젝트는 다음과 같은 Python 프로그래밍 개념을 학습하는데 도움이 됩니다:
- OOP (객체 지향 프로그래밍)
- GUI 프로그래밍
- 이벤트 처리
- 파일 입출력
- 네트워크 프로그래밍
- 예외 처리
