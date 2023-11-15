from PIL import Image, ImageDraw, ImageFont
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s : %(message)s')

PATH = os.path.dirname(os.path.abspath(__file__))
imgFoders = os.path.join(PATH, 'imgFolders')
os.makedirs(imgFoders, exist_ok=True)
def drawIMG(start=1, isCount=8, isCombine=5):
    if start == 0:
        start = 1
    baseIMGFolder = os.path.join(os.getcwd(), 'base\inputIMG')
    fontStyle = 'arial.ttf'
    baseIMG = os.path.join(baseIMGFolder, 'baseIMG.png')
    count_img = 0
    isLoop = 0
    current_img_count = start
    tap = start
    while True:
        count_img += 1
        if count_img == isCombine:
            
            isLoop += 1
            img = Image.open(baseIMG)
            endIMG = start + 3
            d = ImageDraw.Draw(img)
            fnt = ImageFont.truetype(fontStyle, 200)
            d.text((110, 200), f'#{current_img_count}',
                   font=fnt, fill="#ff0000")
            img.save(f'{imgFoders}\Chuong #{tap}.png')
            logging.info(
                f'Save image chuong #{tap}.png save success')
            tap +=1
            start += count_img
            current_img_count +=1
            count_img = 0
            if isLoop >= isCount:
                break
