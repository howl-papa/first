# Fashion AI Strategy

This project analyzes fashion demand with help from Azure OpenAI and provides a simple Gradio interface.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the Gradio app:

```bash
python3 app.py
```

Upload a CSV with `Date`, `SKU`, and `Demand` columns, select the SKU, enter additional variables, and generate a PDF report containing the demand chart and GPT analysis.
