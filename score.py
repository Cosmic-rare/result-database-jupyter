import os
import time
from PIL import Image
import pyocr
import numpy as np
import pyocr.builders
import matplotlib.pyplot as plt
import math
import requests
import io

# path_tesseract = "C:\\Program Files\\Tesseract-OCR"
# if path_tesseract not in os.environ["PATH"].split(os.pathsep):
#     os.environ["PATH"] += os.pathsep + path_tesseract

tools = pyocr.get_available_tools()
tool = tools[0]

def score(url):
    img = Image.open(io.BytesIO(requests.get(url).content))
    rgb_img = img.convert('RGB')
    size = rgb_img.size

    crop_img = rgb_img.crop([0, size[1]/6, size[0]/2, size[1]/2])
    crop_size = crop_img.size

    img2 = Image.new('RGBA',crop_size)

    for x in range(crop_size[0]):
        for y in range(crop_size[1]):
            r,g,b = crop_img.getpixel((x,y))

            if 225 <= r <= 255 and 55 <= g <= 115 and 140 <= b <= 200:
                g = 0
            else:
                g = 255

            img2.putpixel((x,y),(g,g,g,255))

    builder = pyocr.builders.TextBuilder(tesseract_layout=7)
    result = tool.image_to_string(img2, lang="eng", builder=builder)
    return result
