# Dog Breed Quiz Game (강아지 품종 맞추기)

Dog CEO API를 활용한 Python Tkinter 기반의 강아지 품종 맞추기 게임 프로젝트입니다.
무작위로 제공되는 강아지 사진을 보고, 주어진 4개의 선택지 중 올바른 품종을 맞추는 방식의 미니 게임입니다.

## 프로젝트 개요

이 프로젝트는 외부 REST API 통신, GUI 프로그래밍, 그리고 사용자 친화적인 UX 구현을 목표로 합니다. uv 패키지 매니저를 사용하여 재현 가능한 개발 환경을 구성하였으며, 난이도 선택 및 이미지 확대 보기 등 다양한 기능을 포함하고 있습니다.

## 주요 기능

1. 난이도 선택 시스템
   - 사용자는 게임 시작 시 10문제, 20문제, 50문제 중 원하는 난이도를 선택할 수 있습니다.
   - 선택한 문항 수에 따라 게임의 호흡을 조절할 수 있으며, 각 난이도별로 최고 점수가 별도의 파일(dog_game_highscore_xx.txt)에 영구 저장됩니다.

2. 이미지 확대 보기
   - 퀴즈에 나오는 이미지가 작아 식별이 어려운 경우를 대비하여 확대 기능을 구현했습니다.
   - 이미지를 클릭하면 별도의 팝업 창에서 고해상도 이미지를 확인할 수 있습니다.
   - 마우스 커서 변경 및 안내 문구를 통해 상호작용 가능함을 사용자에게 알립니다.

3. 사용자 경험(UX) 및 안정성 개선
   - 로딩 인디케이터: API 응답 대기 시간 동안 "강아지 섭외 중..."과 같은 상태 메시지를 표시하여 프로그램이 멈춘 것처럼 보이는 현상을 방지했습니다.
   - 반응형 레이아웃: 윈도우 해상도를 600x900으로 최적화하고 창 크기 조절을 허용하여, 특정 해상도에서 버튼이 잘리는 UI 버그를 해결했습니다.
   - 즉각적인 피드백: 정답 및 오답 여부를 텍스트와 색상 변화로 즉시 제공합니다.

## 기술 스택

- Language: Python 3.13
- GUI Framework: Tkinter (Python Standard Library)
- HTTP Client: Requests
- Image Processing: Pillow (PIL)
- Dependency Manager: uv
- API: Dog CEO API (Public)

## 프로젝트 구조

├── dog_breed.py         # 게임 메인 실행 파일
├── pyproject.toml       # 프로젝트 의존성 및 메타데이터 설정
├── uv.lock              # 의존성 버전 잠금 파일 (재현성 보장)
├── README.md            # 프로젝트 설명서

## 실행 방법

이 프로젝트는 uv를 통해 의존성을 관리합니다. 아래 절차에 따라 실행환경을 구성해 주세요.

1. 저장소 클론 (Clone Repository)
   git clone https://github.com/QIEclass2025/repo_yoonmo.git
   cd repo_yoonmo

2. 의존성 동기화 (Sync Dependencies)
   pyproject.toml 및 uv.lock 파일을 기반으로 가상환경을 생성하고 라이브러리를 설치합니다.
   uv sync

3. 게임 실행 (Run Game)
   uv run dog_breed.py

## 참고 사항

- 본 프로그램은 인터넷 연결이 필요합니다 (이미지 실시간 다운로드).
- 별도의 API Key 발급 없이 실행 가능합니다.