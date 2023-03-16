import os
from PIL import Image
import pyocr
import pyocr.builders
import math
import difflib
import json
from open import openImg

path_tesseract = 'C:\\Program Files\\Tesseract-OCR'
if path_tesseract not in os.environ['PATH'].split(os.pathsep):
  os.environ['PATH'] += os.pathsep + path_tesseract

tools = pyocr.get_available_tools()
tool = tools[0]

builder1 = pyocr.builders.TextBuilder(tesseract_layout=6)
builder1.tesseract_configs.append('-c')
builder1.tesseract_configs.append('tessedit_char_whitelist="EASYNORMLHDXPT"')

builder2 = pyocr.builders.TextBuilder(tesseract_layout=7)
builder2.tesseract_configs.append('-c')
builder2.tesseract_configs.append('tessedit_char_whitelist="EASYNORMLHDXPT"')

builder3 = pyocr.builders.TextBuilder(tesseract_layout=6)

builder4 = pyocr.builders.TextBuilder(tesseract_layout=7)

def check(target):
  difficults = ['EASY', 'NORMAL', 'HARD', 'EXPERT', 'MASTER']

  data = {'credibility': 0, 'musicDifficulty': ''}

  for j in difficults:
    result = difflib.SequenceMatcher(None, target, j).ratio()

    if result > data['credibility']:
      data['musicDifficulty'] = j
      data['credibility'] = result

  data['ocr'] = target

  return data


def difficult(url):
  img = openImg(url)
  rgb_img = img.convert('RGB')
  size = rgb_img.size
  datas = {}

  for k in range(1,5):
    datas['builder' + str(k)] = {}

  crop_img = rgb_img.crop([0, 0, size[0] / 2, size[1] / 7])
  crop_size = crop_img.size

  resize_img = crop_img.resize(
    (math.floor(crop_size[0] / 15), math.floor(crop_size[1] / 15))
  )

  img2 = Image.new('RGBA', crop_size)

  for x in range(crop_size[0]):
    for y in range(crop_size[1]):
      r, g, b = crop_img.getpixel((x, y))

      if 94 < r < 175 and 179 < g < 255 and 28 < b < 108:
        a = 0
      elif 54 < r < 134 and 144 < g < 224 and 192 < b < 255:
        a = 0
      elif 204 < r < 255 and 135 < g < 215 and 21 < b < 101:
        a = 0
      elif 180 < r < 255 and 42 < g < 122 and 64 < b < 144:
        a = 0
      elif 132 < r < 212 and 22 < g < 102 and 190 < b < 255:
        a = 0
      else:
        a = 255

      img2.putpixel((x, y), (a, a, a, 255))

  for j in range(1,5):
    result = tool.image_to_string(img2, lang='eng', builder=eval('builder' + str(j)))
    datas['builder' + str(j)] = check(result)

  return datas
