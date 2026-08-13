# AI 심화 교육 (ai-advanced-03)

AI 심화 교육 자료 저장소입니다. (day01 ~ day04)

## 커리큘럼

| Day | 주제 | 주요 내용 |
|-----|------|----------|
| [day01](./day01/) | 딥러닝 기초 | 과정 소개, 개발환경 구축(uv), 딥러닝, CNN, 객체탐지, RNN/LSTM |
| [day02](./day02/) | LLM 이해 | Attention, Transformer, LLM, NVIDIA LLM |
| [day03](./day03/) | RAG | RAG 개요, 청킹/저장, 검색, 2026 세제개편안 실습 데이터 |
| [day04](./day04/) | AI Agent · n8n | Agent 개요, n8n 기초, 주식리포트/장바구니 Agent, 실무 유즈케이스 13종 |

## 폴더 구조

각 day 폴더는 공통적으로 다음과 같이 구성됩니다.

- `lecture-materials/` — 강의 교안 (pptx)
- `examples/` — 실습 노트북(ipynb) 및 워크플로우(json)
- day01 `detect_img/` — 객체탐지 실습 이미지
- day03 `tax_data/` — RAG 실습용 2026 세제개편안 문서 (hwpx/pdf)
- day04 `n8n_usecase/` — n8n 실무 유즈케이스 (워크플로우 json + README + 스크린샷)

## 실습 환경 설정

Python 3.11 (권장 3.11.9) / Windows / CPU 기준입니다.

```bash
uv venv --python 3.11
uv pip install -r requirements.txt
```

uv가 처음이라면 `day01/uv_install.bat` 실행 후 위 명령을 수행하세요.

## n8n 실무 유즈케이스

각 유즈케이스 폴더의 README에 워크플로우 설명과 스크린샷이 있습니다.
([day04/n8n_usercase.html](./day04/n8n_usercase.html)에서도 같은 목록을 볼 수 있습니다.)

| # | 워크플로우 / Workflow | 주요 서비스 / Services | 링크 / Link |
|---|-----------|------------|------|
| 02 | 농수산물 시세 AI Agent | KAMIS API, Google Sheets | [바로가기](./day04/n8n_usecase/02-workflow-farm-data/) |
| 03 | Slack 근태 관리 자동화 | Slack, Google Sheets | [바로가기](./day04/n8n_usecase/03-workflow-attendance/) |
| 04 | 회의록 자동 요약 | 음성 인식, AI, Notion, Slack | [바로가기](./day04/n8n_usecase/04-workflow-meeting-assistant/) |
| 05 | 이메일 자동 분류 및 일정 관리 | Gmail, Google Calendar, Google Sheets | [바로가기](./day04/n8n_usecase/05-workflow-email-data/) |
| 06 | 예약 알림 시스템 | 웹앱, DB | [바로가기](./day04/n8n_usecase/06-workflow-reservation-system-data/) |
| 07 | 서울 공공자전거 재고 관리 | 공공 API, KakaoTalk | [바로가기](./day04/n8n_usecase/07-workflow-inventory-bicycle/) |
| 08 | 자동 가계부 | SMS, Google Sheets | [바로가기](./day04/n8n_usecase/08-workflow-automatic-account-book/) |
| 09 | 지능형 파일 정리 | AI 분류, Google Drive, Google Sheets | [바로가기](./day04/n8n_usecase/09-workflow-file-organizer/) |
| 10 | 주식 포트폴리오 리포트 | 주가 API, Gmail | [바로가기](./day04/n8n_usecase/10-workflow-Stock-Portfolio-Report-data/) |
| 11 | OCR 문서 텍스트 추출 | Upstage OCR, Google Sheets | [바로가기](./day04/n8n_usecase/11-workflow-OCR/) |
| 12 | 신규 직원 온보딩 자동화 | Gmail, Slack, DB | [바로가기](./day04/n8n_usecase/12-workflow-onboarding-system/) |
| 13 | Google Sheets 버전 관리 및 복구 | Google Sheets, Slack | [바로가기](./day04/n8n_usecase/13-workflow-google-sheet-manager/) |
| 14 | 날씨 기반 옷차림 추천 챗봇 | 날씨 API, AI Chat | [바로가기](./day04/n8n_usecase/14-workflow-AI-Outfit-Concierge-Chatbot/) |
