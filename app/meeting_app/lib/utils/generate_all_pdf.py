from fpdf import FPDF

def fix_text(text):
    replacements = {
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&quot;": "\"",
        "&#x27;": "'",
        "&#x2F;": "/",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text
    

def generate_pdf_for_all(resume, output_file):
    print(resume)
    pdf = FPDF()
    pdf.add_font("DejaVuSans", fname="font/DejaVuSans.ttf", style="")
    pdf.add_font("DejaVuSans", fname="font/DejaVuSans-Bold.ttf", style="B")
    pdf.add_font("DejaVuSans", fname="font/DejaVuSans-Oblique.ttf", style="I")

    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("DejaVuSans", size=12)

    # Titre
    pdf.set_font("DejaVuSans", "B", 16)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(200, 10, txt=fix_text(resume["title"]), ln=True, align="C")
    pdf.ln(5)

    # Date et durée
    pdf.set_font("DejaVuSans", "I", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(213, 233, 245)
    pdf.cell(0, 8, f"Date: {fix_text(resume['date'])}", ln=True, align="L", fill=True)
    pdf.cell(
        0, 8, f"Duration: {fix_text(resume['duration'])} seconds", ln=True, align="L", fill=True
    )
    pdf.ln(5)

    # Participants
    pdf.set_font("DejaVuSans", "B", 12)
    pdf.set_text_color(0, 102, 204)
    pdf.multi_cell(200, 10, txt="Attendees:", align="L")
    pdf.set_font("DejaVuSans", "I", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(240, 240, 240)
    participants_text = ", ".join([fix_text(attendee) for attendee in resume["attendees"]])
    pdf.cell(0, 10, txt=participants_text, ln=True, align="L", fill=True)
    pdf.ln(5)

    # Résumé
    pdf.set_font("DejaVuSans", "B", 12)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(200, 10, txt="Summary:", ln=True, align="C")
    pdf.set_font("DejaVuSans", size=12)
    pdf.set_text_color(51, 51, 51)
    pdf.multi_cell(0, 5, fix_text(resume["text_sum_up"]))
    pdf.ln(5)

    # Messages
    pdf.set_font("DejaVuSans", "B", 12)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(200, 10, txt="All Messages:", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("DejaVuSans", size=12)
    for message in resume["messages"]:
        # message[user] and message[content]
        pdf.set_font("DejaVuSans", "I", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(200, 10, txt=f"{fix_text(message['user'])}", ln=True, align="L")
        pdf.set_font("DejaVuSans", size=12)
        pdf.set_text_color(51, 51, 51)
        pdf.cell(0, 5, fix_text(message["content"]), align="L")

    pdf.output(output_file)
