---

## 🚀 실행 방법 (Quick Start)

이 프로젝트는 **Azure OpenAI GPT 기반의 패션 수요예측 및 전략 인사이트 생성 도구**입니다.  
Python 3 환경에서 실행되며, CLI 또는 Gradio UI 방식 중 선택적으로 사용할 수 있습니다.

---

### 📦 1. 의존 패키지 설치

먼저 필요한 Python 라이브러리를 설치하세요:

```bash
pip install -r requirements.txt
```

※ `requirements.txt`는 CLI 또는 Gradio 앱이 있는 폴더에서 각각 실행해주세요.

---

### 🔐 2. Azure OpenAI API 환경 변수 설정

GPT 호출을 위해 `gpt_connector.py`는 아래 환경변수를 참조합니다:

```python
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
```

#### ✅ 설정 방법 ①: .env 파일 사용 (권장)

루트 폴더에 `.env` 파일을 생성하고 아래처럼 설정합니다:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_DEPLOYMENT=gpt-4-model-name
```

#### ✅ 설정 방법 ②: 시스템 환경 변수로 직접 입력

```bash
export AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
export AZURE_OPENAI_API_KEY=your_api_key_here
export AZURE_OPENAI_DEPLOYMENT=gpt-4-model-name
```

---

### 🧪 3. 실행 방법

#### ✅ CLI 스크립트 실행

패션 수요예측 분석을 터미널에서 실행하려면:

```bash
python3 fashion_demand_analysis.py
```

- CSV 파일을 입력하면 수요 데이터 분석 및 GPT 전략 인사이트가 출력됩니다.
- 결과는 터미널 또는 PDF로 저장됩니다.

---

#### ✅ Gradio 웹 앱 실행

웹 브라우저 인터페이스를 사용하려면:

```bash
cd fashion-ai-strategy/
pip install -r requirements.txt
python3 app.py
```

- CSV 업로드, 외생 변수(광고비, 날씨, 요일 등) 입력, SKU 선택이 가능합니다.
- 수요 시각화 및 GPT 전략 인사이트가 제공되며, PDF 보고서로 저장됩니다.

---

### 📂 프로젝트 디렉터리 구조

```
fashion-ai-strategy/
├── app.py                  # Gradio 웹앱 실행
├── fashion_demand_analysis.py  # CLI 실행용 스크립트
├── gpt_connector.py        # Azure OpenAI 연결 모듈
├── plot_generator.py       # 수요 그래프 생성
├── report_generator.py     # PDF 리포트 생성
├── requirements.txt        # 의존 패키지 목록
└── .env                    # (선택) 환경 변수 설정 파일
```

---

### ⚠️ 주의 사항

- `.env` 또는 환경 변수 설정이 누락되면 GPT 호출이 실패합니다.
- GPT 호출에는 비용이 발생하니, 사용량에 유의하세요.
- CSV 파일은 최소 `Date`, `SKU`, `Demand` 컬럼을 포함해야 합니다.
- Gradio UI 사용 시 웹브라우저에서 로컬 서버에 접속하게 됩니다 (`localhost:7860` 등).

---

### 🛠️ 디버깅 팁

- 실행 중 문제가 생기면, `[LOG]`로 시작하는 콘솔 로그를 확인하세요.
- GPT API 호출 에러, PDF 저장 오류 등이 구체적으로 표시됩니다.
- 에러 메시지를 복사해서 ChatGPT 또는 Codex에 붙여넣으면 빠른 해결이 가능합니다.

---

