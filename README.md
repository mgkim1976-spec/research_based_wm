# Mirae Asset PB Copilot (Stage 1) - Research Based WM

본 프로젝트는 리서치 센터의 전문 리포트와 스마트머니 유튜브 콘텐츠를 결합하여, PB(Private Banker)들이 고객에게 최적화된 자산 관리 자문을 제공할 수 있도록 지원하는 **하이브리드 영업 지원 시스템**입니다.

## 🚀 Key Features

### 1. 하이브리드 컨텐츠 결합 (Research + Video)
- **리서치 크롤링**: 미래에셋 리서치 센터의 최신 리포트를 실시간으로 수집합니다.
- **유튜브 연동**: '미래에셋 스마트머니' 채널의 최신 시황 영상을 리포트와 매칭합니다.
- **AI 분석**: OpenAI 기반 엔진이 리포트의 핵심 Thesis와 영상의 주요 내용을 분석하여 결합된 인사이트를 도출합니다.

### 2. 고객 세그먼트별 맞춤형 루틴 (Routing Engine)
고객의 자산 규모와 거래 빈도에 따라 4단계 세그먼트(S1~S4)로 분류하고 최적의 영업 루틴을 제안합니다.
- **S1 (휴면/초보)**: 영상 중심의 쉬운 접근, 기초 교육 루틴(D)
- **S2 (액티브/유망)**: 트렌드 민감, 일간 모닝(A) 및 테마 루틴(C)
- **S3 (안정형/고액)**: 보수적 자산가, 격주 전문 분석(B) 및 심층 관리
- **S4 (VIP/전문가)**: 고도의 전문성 보유, 전 루틴(A~D)을 VVIP 관점에서 타격

### 3. 지능형 영업 지원 도구
- **AI 메시지 드래프트**: 고객 세그먼트에 맞춘 카카오톡/메시지 초안 자동 생성 (한글화 완료).
- **콘텐츠 가변 대응**: 영상 유무에 따라 [영상 링크] 포함 여부 및 권장 액션(CTA)이 유연하게 변경됩니다.
- **보안 우회 URL**: PB가 별도의 보안 모듈 설치 없이도 리포트 원본을 즉시 확인할 수 있는 UX를 제공합니다.

### 4. 우선순위(Priority) 체계
- **P1 ~ P10 점수**: 루틴의 적합도와 긴급도를 수치화하여 PB가 가장 먼저 대응해야 할 고객(P8~P10)을 대시보드 상단에 배치합니다.

## 🛠 Tech Stack
- **Backend**: Python, Flask
- **AI**: OpenAI API (GPT-4.1-mini)
- **Scraping**: BeautifulSoup, Requests
- **Frontend**: HTML5, Vanilla CSS (Tailwind CSS CDN), JavaScript

## 📂 Project Structure
```text
.
├── app/
│   ├── core/
│   │   ├── adapters/     # Crawler, Youtube Connector
│   │   ├── ai/           # OpenAI Engine
│   │   ├── engine/       # Matcher, Segment Router
│   │   └── workflows/    # Routine Orchestrator (A, B, C, D)
│   ├── templates/        # Dashboard (index.html), Guide (guide.html)
│   └── app.py            # Flask Main Entry
├── data/                 # Stored Research JSON DB
└── README.md
```

## 📖 How to Use
1. **대시보드**: 오늘 가장 주목해야 할 하이브리드 번들(리서치+영상)을 확인합니다.
2. **고객 타겟팅**: AI가 우선순위(P점수)에 따라 정렬한 고객 명단을 확인하고 메시지 초안을 복사합니다.
3. **루틴 교체**: '다른 리서치 후보' 목록에서 원하는 리포트로 오늘의 루틴을 즉시 변경할 수 있습니다.
4. **워크플로우 가이드**: 'PB Workflow 가이드' 메뉴에서 세그먼트별 상세 전략을 학습합니다.

---
*본 시스템은 미래에셋 PB의 디지털 영업 경쟁력 강화를 위해 개발되었습니다.*
