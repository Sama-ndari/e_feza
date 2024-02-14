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
    photo_path = f"static/{photo.filename}"
    photo.save(photo_path)

    # Générer la badge
    badge = generate_badge(nom, prenom, code_agent, numero_telephone, photo_path, format_=format_choisi)

    if format_choisi == "pdf":
        return send_file(badge, as_attachment=True)
    else:
        return send_file("static/badge.png", as_attachment=True)


def generate_badge(nom, prenom, code_agent, numero_telephone, photo_path, format_):
    # on cree la badge
    badge = generate_badge_image(nom, prenom, code_agent, numero_telephone, photo_path)
    if format_ == "pdf":
        # recuperer l'image de la badge
        pdf_path = os.path.join("static", "badge.pdf")
        c = canvas.Canvas(pdf_path, pagesize=landscape(A6))

        # Dessiner le badge dans le canvas PDF
        photo = "static/badge.png"
        c.drawImage(photo, 10, 50, width=319, height=232)

        c.showPage()
        c.save()
        return pdf_path
    else:
        return badge


def generate_badge_image(nom, prenom, code_agent, numero_telephone, photo_path):
    # Charger le modèle de badge, l image donc
    badge = Image.open("static/images/badge.jpg")
    draw = ImageDraw.Draw(badge)

    font_petit = ImageFont.truetype("oswald.light.ttf", size=15)
    font_grand = ImageFont.truetype("oswald.bold.ttf", size=22)
    blue1_color = (0, 101, 148)
    blue2_color = (8, 53, 83)
    text_x = 145
    text_y = 70
    draw.text((text_x, text_y - 2), f"{nom}", font=font_grand, fill=blue1_color)
    draw.text((text_x, text_y + 33), f"{prenom}", font=font_petit, fill=blue2_color)
    draw.text((text_x, text_y + 59), f"Code Agent: {code_agent}", font=font_petit, fill=blue2_color)
    draw.text((text_x, text_y + 86), f"📞 {numero_telephone}", font=font_petit, fill=blue2_color)

    # Ajout de la photo du user sur la badge
    user_pic = Image.open(photo_path)
    resized_pic = user_pic.resize((105, 123))
    badge.paste(resized_pic, (27, 79))

    # Ajout du logo de eFeza sur la badge
    logo = Image.open("static/images/logo_badge.png")
    resize_logo = logo.resize((100, 40))
    badge.paste(resize_logo, (215, 180))

    # Enregistrer la badge généré en tant qu'image
    badge_path = os.path.join("static/badge.png")
    badge.save(badge_path)
    return badge


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
