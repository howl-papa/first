from fpdf import FPDF


def create_report(image_path: str, insight: str, output_file: str) -> None:
    """Create PDF report with chart image and GPT insight."""
    print(f"Saving report to {output_file}")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Fashion Demand Analysis", ln=True)
    pdf.image(image_path, w=170)
    pdf.ln(85)
    pdf.multi_cell(0, 10, insight)
    pdf.output(output_file)
