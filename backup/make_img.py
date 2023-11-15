from PIL import Image
import re, os


# sorted file in folder
def sorted_alphanumeric(data):
    def convert(text): return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)

PATH = os.path.dirname(os.path.abspath(__file__))
img_folder = os.path.join(PATH,'img')
images = []
for img_item in sorted_alphanumeric(os.listdir(img_folder)):
    img_path = os.path.join(img_folder, img_item)
    images.append(Image.open(img_path))
# images = [, Image.open("image2.png"), Image.open("image3.png")]

pdf_path = "output.pdf"

images[0].save(pdf_path, "PDF" ,resolution=150.0, save_all=True, append_images=images[1:])