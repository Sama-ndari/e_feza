from flask import Flask, render_template, request, send_file
import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import landscape, A6
from reportlab.pdfgen import canvas

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate_badge", methods=["POST"])
def generate():
    # Récupérer les données du formulaire
    nom = request.form["nom"].title()
    prenom = request.form["prenom"].title()
    code_agent = request.form["code"]
    numero_telephone = request.form["numero"]
    photo = request.files["photo"]
    format_choisi = request.form["format"]

    # Enregistrer la photo du user sur le serveur
    # photo_path = os.path.join("static", "uploads", photo.filename)
    photo_path = f"static/uploads/{photo.filename}"
    photo.save(photo_path)

    # Générer la badge
    badge = generate_badge(nom, prenom, code_agent, numero_telephone, photo_path, format_=format_choisi)

    if format_choisi == "pdf":
        return send_file(badge, as_attachment=True)
    else:
        # Enregistrer la badge généré en tant qu'image
        badge_path = os.path.join("static/badge.png")
        badge.save(badge_path)
        return send_file("static/badge.png", as_attachment=True)


def generate_badge(nom, prenom, code_agent, numero_telephone, photo_path, format_):
    if format_ == "pdf":
        # le badge au format PDF
        pdf_path = os.path.join("static", "badge.pdf")
        c = canvas.Canvas(pdf_path, pagesize=landscape(A6))

        # Dessiner le badge dans le canvas PDF
        c.drawImage(photo_path, 40, 140, width=120, height=150)
        c.drawImage("static/images/logo.png", 300, 240, width=120, height=60)

        font_petit = "Helvetica", 14
        font_grand = "Helvetica-Bold", 24
        blue1_color = (0, 101, 148)
        blue2_color = (0, 176, 240)
        text_x = 200
        text_y = 220
        c.setFont(*font_grand)
        c.setFillColor(blue2_color)
        c.drawString(text_x, text_y, nom)
        c.setFont(*font_petit)
        c.setFillColor(blue1_color)
        c.drawString(text_x, text_y - 30, prenom)
        c.drawString(text_x, text_y - 60, f"Code Agent: {code_agent}")
        c.drawString(text_x, text_y - 80, f"📞 {numero_telephone}")

        c.showPage()
        c.save()
        return pdf_path
    else:
        # Charger le modèle de badge, l image donc
        badge = Image.open("static/images/badge_template2.png")
        draw = ImageDraw.Draw(badge)

        font_petit = ImageFont.truetype("arial.ttf", size=20)
        font_grand = ImageFont.truetype("arial.ttf", size=36)
        blue1_color = (0, 101, 148)
        blue2_color = (8, 53, 83)
        # blue3_color = (68, 158, 215)
        text_x = 450
        text_y = 500
        draw.text((text_x, text_y), f"{nom}", font=font_grand, fill=blue1_color)
        draw.text((text_x + 10, text_y + 40), f"{prenom}", font=font_petit, fill=blue2_color)
        draw.text((text_x, text_y + 80), f"Code Agent: {code_agent}", font=font_petit, fill=blue2_color)
        draw.text((text_x, text_y + 110), f"📞 {numero_telephone}", font=font_petit, fill=blue2_color)

        # Ajout de la photo du user sur la badge
        user_pic = Image.open(photo_path)
        resized_pic = user_pic.resize((200, 250))
        badge.paste(resized_pic, (200, 380))

        # Ajout du logo de eFeza sur la badge
        logo = Image.open("static/images/logo.png")
        resize_logo = logo.resize((200, 100))
        badge.paste(resize_logo, (450, 380))

        return badge


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
