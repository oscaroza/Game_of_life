# Import the library we will use to manipulates images
from PIL import Image

# Creation of an RGB 300x300 pixels images
img = Image.new("RGB", (506, 506))

# Loop over each puixel to initialize the colour of each of them
for x in range(506):
    for y in range(506):

        # Setting each pixel black
        img.putpixel((x, y), (80, 80, 80))

img.save("first_image.png")
# We prefer images woth format .png which are less heavy than .jpg for what we are doing
# The difference is for transparent backgrounds, which we won't have.

show = input("Do you want to show the image ? (y/n) : ")
if show == "y":
    img.show()