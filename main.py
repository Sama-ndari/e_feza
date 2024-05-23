from flask import Flask, render_template, request, send_file
import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import portrait, A6
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

    if format_ == "pdf":
        # on cree la badge
        badge = generate_badge_pdf(nom, prenom, code_agent, numero_telephone, photo_path)
        # recuperer l'image de la badge
        pdf_path = os.path.join("static", "badge.pdf")
        c = canvas.Canvas(pdf_path, pagesize=portrait(A6))

        # Dessiner le badge dans le canvas PDF
        photo = "static/badge_pdf.png"
        c.drawImage(photo, 25, 50, width=229, height=344)

        c.showPage()
        c.save()
        return pdf_path
    else:
        # on cree la badge sous forme d image
        badge = generate_badge_image(nom, prenom, code_agent, numero_telephone, photo_path)
        return badge


def generate_badge_pdf(nom, prenom, code_agent, numero_telephone, photo_path):
    # Charger le modèle de badge, l image donc
    badge = Image.open("static/images/badge_portrait_pdf.jpg")
    draw = ImageDraw.Draw(badge)

    font_arial = ImageFont.truetype("arial.ttf", size=25)
    font_petit = ImageFont.truetype("oswald.light.ttf", size=35)
    font_grand = ImageFont.truetype("oswald.bold.ttf", size=40)
    blue1_color = (0, 101, 148)
    blue2_color = (8, 53, 83)
    text_x = 60
    text_y = 490
    draw.text((text_x, text_y + 8), "Nom : ", font=font_arial, fill=blue2_color)
    draw.text((text_x, text_y + 48), "Prenom : ", font=font_arial, fill=blue2_color)
    draw.text((text_x, text_y + 88), "Code-Agent : ", font=font_arial, fill=blue2_color)
    draw.text((text_x, text_y + 128), "Numero : ", font=font_arial, fill=blue2_color)
    draw.text((text_x + 80, text_y - 15), f"{nom}", font=font_grand, fill=blue1_color)
    draw.text((text_x + 120, text_y + 30), f"{prenom}", font=font_petit, fill=blue2_color)
    draw.text((text_x + 160, text_y + 70), f"{code_agent}", font=font_petit, fill=blue2_color)
    draw.text((text_x + 120, text_y + 110), f"{numero_telephone}", font=font_petit, fill=blue2_color)

    # Ajout de la photo du user sur la badge
    user_pic = Image.open(photo_path)
    resized_pic = user_pic.resize((250, 315))
    badge.paste(resized_pic, (120, 160))

    # Ajout du logo de eFeza sur la badge
    logo = Image.open("static/images/logo_badge.png")
    resize_logo = logo.resize((300, 120))
    badge.paste(resize_logo, (70, 40))

    # Enregistrer la badge généré en tant qu'image
    badge_path = os.path.join("static/badge_pdf.png")
    badge.save(badge_path)
    return badge


def generate_badge_image(nom, prenom, code_agent, numero_telephone, photo_path):
    # Charger le modèle de badge, l image donc
    badge = Image.open("static/images/badge_portrait.jpg")
    draw = ImageDraw.Draw(badge)

    font_arial = ImageFont.truetype("arial.ttf", size=25)
    font_petit = ImageFont.truetype("oswald.light.ttf", size=35)
    font_grand = ImageFont.truetype("oswald.bold.ttf", size=40)
    blue1_color = (0, 101, 148)
    blue2_color = (8, 53, 83)
    text_x = 120
    text_y = 590
    draw.text((text_x, text_y + 8), "Nom : ", font=font_arial, fill=blue2_color)
    draw.text((text_x, text_y + 48), "Prenom : ", font=font_arial, fill=blue2_color)
    draw.text((text_x, text_y + 88), "Code-Agent : ", font=font_arial, fill=blue2_color)
    draw.text((text_x, text_y + 128), "Numero : ", font=font_arial, fill=blue2_color)
    draw.text((text_x + 80, text_y - 15), f"{nom}", font=font_grand, fill=blue1_color)
    draw.text((text_x + 120, text_y + 30), f"{prenom}", font=font_petit, fill=blue2_color)
    draw.text((text_x + 160, text_y + 70), f"{code_agent}", font=font_petit, fill=blue2_color)
    draw.text((text_x + 120, text_y + 110), f"{numero_telephone}", font=font_petit, fill=blue2_color)

    # Ajout de la photo du user sur la badge
    user_pic = Image.open(photo_path)
    resized_pic = user_pic.resize((200, 260))
    badge.paste(resized_pic, (175, 310))

    # Ajout du logo de eFeza sur la badge
    logo = Image.open("static/images/logo_badge.png")
    resize_logo = logo.resize((250, 100))
    badge.paste(resize_logo, (150, 180))

    # Enregistrer la badge généré en tant qu'image
    badge_path = os.path.join("static/badge.png")
    badge.save(badge_path)
    return badge


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
