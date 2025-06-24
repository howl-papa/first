import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from fpdf import FPDF
import requests
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
def load_data(file_path: str) -> pd.DataFrame:
    """Load CSV file containing Date, SKU, Demand."""
    logging.info("Loading data from %s", file_path)
    df = pd.read_csv(file_path, parse_dates=['Date'])
    return df

def select_sku(df: pd.DataFrame) -> str:
    """Display SKUs and return selected SKU."""
    skus = df['SKU'].unique()
    logging.info("Available SKUs: %s", ', '.join(skus))
    for i, sku in enumerate(skus, 1):
        print(f"{i}. {sku}")
    idx = int(input("Select SKU by number: ")) - 1
    return skus[idx]

def filter_data(df: pd.DataFrame, sku: str) -> pd.DataFrame:
    """Filter data for selected SKU and last 30 days."""
    cutoff = datetime.now() - timedelta(days=30)
    mask = (df['SKU'] == sku) & (df['Date'] >= cutoff)
    filtered = df.loc[mask]
    logging.info("Filtered data has %d rows", len(filtered))
    return filtered

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with missing or negative demand."""
    cleaned = df.dropna(subset=['Demand'])
    cleaned = cleaned[cleaned['Demand'] >= 0]
    logging.info("Cleaned data has %d rows", len(cleaned))
    return cleaned

def plot_demand(df: pd.DataFrame, sku: str, filename: str) -> None:
    """Plot demand over time and save as image."""
    logging.info("Plotting demand chart")
    plt.figure(figsize=(8,4))
    plt.plot(df['Date'], df['Demand'], marker='o')
    plt.title(f"Demand for {sku}")
    plt.xlabel("Date")
    plt.ylabel("Demand")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def build_prompt(sku: str, ad_spend: float, weather: str, weekday: str) -> str:
    """Create GPT prompt with business scenario."""
    prompt = (
        f"You are analyzing fashion demand data for SKU {sku}. "
        f"Recent advertising spend was {ad_spend}. "
        f"Weather conditions are {weather}. "
        f"Today is {weekday}. "
        "Provide insights for inventory, marketing, and merchandising in either Korean or English."
    )
    return prompt

def call_azure_openai(prompt: str) -> str:
    """Call Azure OpenAI API to get analysis."""
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
    if not endpoint or not api_key or not deployment:
        logging.warning("Azure OpenAI environment variables not set. Returning placeholder insight.")
        return "[Azure OpenAI credentials missing. Insight unavailable.]"
    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version=2023-07-01-preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    data = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300
    }
    logging.info("Calling Azure OpenAI API")
    resp = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
    if resp.status_code == 200:
        content = resp.json()['choices'][0]['message']['content']
        return content.strip()
    else:
        logging.error("Azure OpenAI API error: %s", resp.text)
        return "[Error fetching insight from Azure OpenAI]"

def save_pdf(image_path: str, insight: str, output_file: str) -> None:
    """Save chart image and GPT insight to PDF."""
    logging.info("Saving results to %s", output_file)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Fashion Demand Analysis", ln=True)
    pdf.image(image_path, w=170)
    pdf.ln(85)
    pdf.multi_cell(0, 10, insight)
    pdf.output(output_file)

def main():
    file_path = input("Enter path to CSV file: ")
    df = load_data(file_path)
    sku = select_sku(df)
    ad_spend = float(input("Enter recent advertising spend: "))
    weather = input("Enter recent weather conditions: ")
    weekday = input("Enter current weekday: ")

    df_filtered = filter_data(df, sku)
    df_clean = clean_data(df_filtered)
    plot_file = "demand_plot.png"
    plot_demand(df_clean, sku, plot_file)

    prompt = build_prompt(sku, ad_spend, weather, weekday)
    insight = call_azure_openai(prompt)

    save_pdf(plot_file, insight, "analysis_result.pdf")
    logging.info("Analysis complete. Output saved to analysis_result.pdf")

if __name__ == "__main__":
    main()
