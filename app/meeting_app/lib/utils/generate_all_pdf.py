from fpdf import FPDF

def generate_pdf_for_all(resume, output_file):
    print(resume)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    # Titre
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(200, 10, txt=resume['title'], ln=True, align="C")
    pdf.ln(5)

    # Date et durée
    pdf.set_font("Arial", 'I', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(213, 233, 245)
    pdf.cell(0, 8, f"Date: {resume['date']}", ln=True, align="L", fill=True)
    pdf.cell(0, 8, f"Duration: {resume['duration']} seconds", ln=True, align="L", fill=True)
    pdf.ln(5)

    # Participants
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 102, 204)
    pdf.multi_cell(200, 10, txt="Attendees:", ln=True, align="L")
    pdf.set_font("Arial", "I", size=12)
    pdf.set_text_color(0, 0, 0) 
    pdf.set_fill_color(240, 240, 240)
    participants_text = ', '.join(resume['attendees'])
    pdf.cell(0, 10, txt=participants_text, ln=True, align="L", fill=True)
    pdf.ln(5)

    # Résumé
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(200, 10, txt="Summary:", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(51, 51, 51)
    pdf.multi_cell(0, 5, resume['text_sum_up'])
    pdf.ln(5)

    # Messages
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(200, 10, txt="All Messages:", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", size=12)

    pdf.output(output_file)
