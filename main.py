from flask import Flask, render_template, request, send_file
import os
from PIL import Image, ImageDraw, ImageFont

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

    # Enregistrer la photo du user sur le serveur
    photo_path = os.path.join("static", photo.filename)
    photo.save(photo_path)

    # Générer la badge
    badge = generate_badge(nom, prenom, code_agent, numero_telephone, photo_path)

    # Enregistrer la badge généré en tant qu'image
    badge_path = os.path.join("static/badge.png")
    badge.save(badge_path)

    # Retourner le badge généré en tant que fichier qu'on peut telecharger
    return send_file(badge_path, as_attachment=True)


def generate_badge(nom, prenom, code_agent, numero_telephone, photo_path):
    # Charger le modèle de badge, l image donc
    badge = Image.open("static/images/badge_template1.png")
    draw = ImageDraw.Draw(badge)

    font_petit = ImageFont.truetype("arial.ttf", size=20)
    font_grand = ImageFont.truetype("arial.ttf", size=36)
    blue1_color = (0, 101, 148)
    blue2_color = (8, 53, 83)
    # blue3_color = (68, 158, 215)
    text_x = 450
    text_y = 500
    draw.text((text_x, text_y), f"{nom}", font=font_grand, fill=blue1_color)
    draw.text((text_x+10, text_y + 40), f"{prenom}", font=font_petit, fill=blue2_color)
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
    app.run(host='0.0.0.0', port=port)
