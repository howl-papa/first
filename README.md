# 🧵 Fashion Demand Forecasting & Strategic Insight Generator

AI를 활용한 패션 산업의 SKU별 수요 예측과 재고/마케팅/MD 전략 인사이트 자동 생성 도구입니다.  
CSV 파일 기반으로 수요 트렌드를 분석하고, Azure OpenAI GPT-4를 활용해 실질적인 비즈니스 의사결정에 도움을 주는 리포트를 생성합니다.

---

## 🚀 Features

- 📁 **CSV 기반 데이터 업로드 (Date, SKU, Demand)**
- 🎛️ **SKU 선택 및 날짜 필터링 (전체 / 최근 30일)**
- 📊 **수요 추이 시각화 (matplotlib)**
- 📥 **외부 변수 입력 (광고비, 날씨, 요일 등)**
- 🧠 **GPT-4 기반 전략 인사이트 자동 생성**
- 🌐 **한/영 다국어 지원**
- 🧾 **PDF 보고서 자동 저장 (그래프 + 분석 포함)**
- 📈 **Gradio 웹 인터페이스**
- 🐞 **Debug 로그 출력으로 실행 단계 추적 가능**

---

## 🧩 프로젝트 구조

```
fashion-ai-strategy/
├── app.py                     # Gradio 실행 메인 파일
├── data_handler.py            # CSV 처리, 필터링 함수
├── prompt_builder.py          # GPT 프롬프트 생성
├── gpt_connector.py           # Azure OpenAI API 연결
├── plot_generator.py          # 수요 시각화 함수
├── report_generator.py        # PDF 리포트 생성
├── requirements.txt
└── README.md
```

---

## 🛠️ Getting Started

### 1. Clone this repository

```bash
git clone https://github.com/your-username/fashion-ai-strategy.git
cd fashion-ai-strategy
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
# .env 파일에 다음 값들을 설정하세요
OPENAI_API_KEY=your_openai_api_key
AZURE_ENDPOINT=your_azure_openai_endpoint
```

### 4. Run the app

```bash
python app.py
```

---

## 🧠 GPT Prompt Example

```text
You are a retail strategy expert. Based on recent 30-day demand data for SKU A001 and the following context:
- Advertising: High
- Weather: Rainy
- Weekday: Sunday
Generate business insights in the areas of:
1. Inventory Strategy
2. Marketing Strategy
3. MD Strategy
Language: Korean
```

---

## 📎 Sample Use Case

> “여름 시즌 반팔 티셔츠 SKU의 판매 추이가 떨어지는데, 광고비를 늘릴지 아니면 재고를 줄여야 할지 결정이 필요하다. 이 툴은 실시간 데이터를 기반으로 최적의 전략을 제시한다.”

---

## ✅ 적용 도메인 및 확장 가능성

- 명품/SPA/내셔널 브랜드 등 다양한 패션 유통망
- 실제 POS/ERP 데이터 연동 PoC
- 광고 예산 시뮬레이션, SKU 리뉴얼 의사결정
- 날씨 API, 프로모션 캘린더 등 확장 연계

---

## 🧾 Output Example

- 수요 추이 그래프 (`.png`)
- PDF 보고서 (GPT 분석 포함)
- SKU 드롭다운 자동 생성

---

## 🧪 개발 중 기능

- Prophet 기반 실제 예측 모델 통합
- 멀티 SKU 분석 및 비교 시각화
- 브랜드 로고 포함 커스터마이징 보고서

---

## 👤 Author

용락 (Yongrak)  
AI + Fashion Strategy Explorer  
[LinkedIn](https://linkedin.com/in/yongrak.pro) | [Email](yongrak.pro@gmail.com)
