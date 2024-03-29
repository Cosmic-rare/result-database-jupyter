import os
from PIL import Image
import pyocr
import pyocr.builders
import difflib
import json
from open import openImg

path_tesseract = 'C:\\Program Files\\Tesseract-OCR'
if path_tesseract not in os.environ['PATH'].split(os.pathsep):
  os.environ['PATH'] += os.pathsep + path_tesseract

tools = pyocr.get_available_tools()
tool = tools[0]

border = 215

builder3 = pyocr.builders.TextBuilder(tesseract_layout=11)

def check(target):
  with open('./json/music.json', encoding='utf-8') as f1:
    music = json.load(f1)

    data = {}
    data2 = []

    for j in music:
      result = difflib.SequenceMatcher(None, target, j['title']).ratio()

      if result > 0.6:
        data2.append({'title': j['title'], 'credibility': result, 'musicId': j['id']})

    data['ocr'] = target
    data['candidate'] = data2
    return data


def title(url):
    img = openImg(url)

    rgb_img = img.convert('RGB')
    size = rgb_img.size

    crop_img = rgb_img.crop([0, 0, size[0] / 2, size[1] / 7])
    crop_size = crop_img.size

    img2 = Image.new('RGBA', crop_size)

    for x in range(crop_size[0]):
      for y in range(crop_size[1]):
        r, g, b = crop_img.getpixel((x, y))

        if r >= border and g >= border and b >= border:
          a = 255
        else:
          a = 0

        img2.putpixel((x, y), (a, a, a, 255))

    crop_range = img2.convert('RGB').getbbox()
    img3 = img2.crop(
        [crop_range[0], crop_range[1] - 5, crop_range[2], (crop_range[3]) / 2]
    )

    data3 = tool.image_to_string(img3, lang='jpn', builder=builder3)

    data3 = data3.replace('\n', '')
    data3 = data3.replace(' ', '')

    data3 = check(data3)
    
    return {'builder3':data3}
