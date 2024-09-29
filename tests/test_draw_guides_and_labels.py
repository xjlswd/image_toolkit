from PIL import Image

from image_toolkit.image_processor import draw_rectangles_with_labels, draw_guides

image_file = "./images/OIP-C.jpg"
image = Image.open(image_file)
draw_guides(image)

draw_rectangles_with_labels(image,((0,0,340,212),(453,520,650,850)),('刀具','打火机'))
image.save("out.jpg")