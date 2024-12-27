from fpdf import FPDF

def generate_pdf_for_message(messages, title,output_file):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 102, 204)  # Bleu pour le titre
    pdf.cell(200, 5, txt=title, ln=True, align="C")
    pdf.ln(1)
    pdf.set_font("Arial", 'I', 12)
    pdf.set_text_color(200, 200, 220)  # Bleu pour le titre
    pdf.cell(200, 10, txt="All messages", ln=True, align="C")
    
    # Définir la police générale pour le texte
    pdf.set_font("Arial", size=12)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 102, 204)  # Couleur pour le titre "Participants"
    pdf.cell(200, 10, txt="Participants:", ln=True, align="L")
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0) 

    pdf.set_fill_color(240, 240, 240) 
    
    participants_text = []
    
    for message in messages: 
        participants_text.append(message['discord_tag'])
        print(message['discord_tag'])
        
    participants_text = ', '.join(participants_text)
        
    pdf.multi_cell(0, 10, txt=f"{participants_text}", ln=True, align="L", fill=True)
    print(participants_text)

    pdf.ln(5)
    
    for message in messages:
        pdf.set_text_color(150,150,210)
        pdf.cell(200,5,f"{message['discord_tag']} - {message['datetime']}:")
        pdf.ln(5)
        pdf.set_text_color(10,10,10)
        pdf.multi_cell(200,5,f"{message['message']}")
        pdf.ln(1)
        
    
    pdf.output(output_file)