from fpdf import FPDF

def generate_pdf_for_all(messages, resume, title, output_file):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Définir la police générale pour le texte
    pdf.set_font("Arial", size=12)

    # Titre principal avec style
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 102, 204)  # Bleu pour le titre
    pdf.cell(200, 10, txt=resume['title'], ln=True, align="C")
    pdf.ln(5)

    # Date et durée dans un encadré avec un style différent
    pdf.set_font("Arial", 'I', 12)  # Italique pour la date et la durée
    pdf.set_text_color(0, 0, 0)  # Noir pour les informations de base
    
    # Encadré pour la date
    pdf.set_fill_color(213, 233, 245)  # Fond gris clair
    pdf.cell(0, 8, f"Date: {resume['date']}", ln=True, align="L", fill=True)
    
    # Encadré pour la durée
    pdf.cell(0, 8, f"Duration: {resume['duration']} seconds", ln=True, align="L", fill=True)
    
    pdf.ln(5)
    
    # Ajouter la liste des participants
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 102, 204)  # Couleur pour le titre "Participants"
    pdf.multi_cell(200, 10, txt="Participants:", ln=True, align="L")
    pdf.set_font("Arial", "I", size=12)
    pdf.set_text_color(0, 0, 0)  # Noir pour la liste des participants

    pdf.set_fill_color(240, 240, 240)  # Fond gris clair

    # Créer une chaîne de texte avec les participants séparés par des virgules
    participants_text = ', '.join(resume['attendees'])

    # Afficher les noms des participants sur une seule ligne
    pdf.cell(0, 10, txt=participants_text, ln=True, align="L", fill=True)

    pdf.ln(5)

    # Résumé avec un style distinct
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(200, 10, txt="Résumé:", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(51, 51, 51)  # Gris pour le texte du résumé
    pdf.multi_cell(0, 5, resume['text_sum_up'])
    
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(200, 10, txt="All Messages:", ln=True, align="C")
    
    pdf.ln(5)
    
    pdf.set_font("Arial",size=12)
    
    for message in messages:
        pdf.set_text_color(150,150,210)
        pdf.cell(200,5,f"{message['discord_tag']} - {message['datetime']}:")
        pdf.ln(5)
        pdf.set_text_color(10,10,10)
        pdf.multi_cell(200,5,f"{message['message']}")
        pdf.ln(1) 
        
    pdf.output(output_file)