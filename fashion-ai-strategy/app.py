import gradio as gr
from data_handler import load_csv, get_sku_list, filter_last_30_days, clean_demand
from prompt_builder import build_prompt
from gpt_connector import call_gpt
from plot_generator import plot_demand
from report_generator import create_report


print("Launching Fashion AI Strategy App")


def update_skus(file):
    if file is None:
        return gr.Dropdown.update(choices=[], value=None)
    try:
        print("[INFO] Loading CSV for SKU dropdown")
        df = load_csv(file.name)
        print(f"[INFO] Loaded dataframe shape: {df.shape}")
        skus = get_sku_list(df)
        print(f"[INFO] {len(skus)} SKUs found")
        return gr.Dropdown.update(choices=skus, value=skus[0] if skus else None)
    except Exception as e:
        print(f"[ERROR] Failed to load CSV: {e}")
        return gr.Dropdown.update(choices=[], value=None)


def run_pipeline(file, sku, ad_spend, weather, weekday):
    print("[INFO] Starting analysis pipeline")
    try:
        print("[INFO] Loading CSV data")
        df = load_csv(file.name)
        print(f"[INFO] Raw data shape: {df.shape}")
    except Exception as e:
        print(f"[ERROR] Failed to read CSV: {e}")
        return None, "[ERROR] Could not read CSV", None

    print("[INFO] Filtering last 30 days data")
    df_filtered = filter_last_30_days(df, sku)
    print(f"[INFO] Filtered data shape: {df_filtered.shape}")

    print("[INFO] Cleaning demand data")
    df_clean = clean_demand(df_filtered)
    print(f"[INFO] Cleaned data shape: {df_clean.shape}")

    plot_file = "demand_plot.png"
    print("[INFO] Generating demand chart")
    plot_demand(df_clean, sku, plot_file)

    print("[INFO] Starting GPT prompt generation...")
    prompt = build_prompt(sku, ad_spend, weather, weekday)
    print(f"[INFO] Prompt preview: {prompt[:100]}")

    try:
        insight = call_gpt(prompt)
        print("[SUCCESS] GPT response received")
        print(f"[INFO] GPT output preview: {insight[:100]}")
    except Exception as e:
        print(f"[ERROR] GPT API call failed: {e}")
        insight = "[ERROR] GPT call failed"

    report_file = "analysis_result.pdf"
    print("[INFO] Saving PDF report")
    try:
        create_report(plot_file, insight, report_file)
        print(f"[SUCCESS] PDF report saved to {report_file}")
    except Exception as e:
        print(f"[ERROR] Failed to save PDF report: {e}")
        report_file = None

    print("[SUCCESS] Pipeline complete")
    return plot_file, insight, report_file


def build_interface():
    with gr.Blocks() as demo:
        file_input = gr.File(label="Upload CSV")
        sku_dropdown = gr.Dropdown(label="SKU", choices=[])
        ad_spend_input = gr.Number(label="Advertising Spend")
        weather_input = gr.Textbox(label="Weather")
        weekday_input = gr.Textbox(label="Weekday")
        run_btn = gr.Button("Run Analysis")
        chart_output = gr.Image(label="Demand Chart")
        insight_output = gr.Textbox(label="GPT Insight")
        pdf_output = gr.File(label="Download Report")

        file_input.change(update_skus, inputs=file_input, outputs=sku_dropdown)
        run_btn.click(run_pipeline,
                      inputs=[file_input, sku_dropdown, ad_spend_input, weather_input, weekday_input],
                      outputs=[chart_output, insight_output, pdf_output])
    return demo


if __name__ == "__main__":
    demo = build_interface()
    demo.launch()
