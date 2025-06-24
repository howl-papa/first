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
    df = load_csv(file.name)
    skus = get_sku_list(df)
    return gr.Dropdown.update(choices=skus, value=skus[0] if skus else None)


def run_pipeline(file, sku, ad_spend, weather, weekday):
    print("Running analysis pipeline")
    df = load_csv(file.name)
    df_filtered = filter_last_30_days(df, sku)
    df_clean = clean_demand(df_filtered)
    plot_file = "demand_plot.png"
    plot_demand(df_clean, sku, plot_file)
    prompt = build_prompt(sku, ad_spend, weather, weekday)
    insight = call_gpt(prompt)
    report_file = "analysis_result.pdf"
    create_report(plot_file, insight, report_file)
    print("Pipeline complete")
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
