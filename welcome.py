from PIL import Image, ImageDraw, ImageFont

# Ouvrir l'image
img = Image.open("Welcome.jpg")  # Assure-toi que le fichier existe ici
draw = ImageDraw.Draw(img)

texte = "Continue>>"

# Police
try:
    font = ImageFont.truetype("Times New Roman", 50)
except:
    font = ImageFont.load_default()

# Calcul taille du texte
bbox = draw.textbbox((0,0), texte, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# Dimensions image
width, height = img.size

# Position texte
x = 1200
y = height - text_height - 50

# Rectangle blanc derrière le texte
draw.rectangle((x - 10, y - 5, x + text_width + 10, y + text_height + 20),
    fill=(255, 255, 255), outline=None)

# Dessiner le texte
draw.text((x, y), texte, fill=(200,0,200), font=font)

# Sauvegarder et afficher
img.save("image_modifiee.jpg")
img.show()