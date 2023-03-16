from lib.templateMatch import get_point
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import os
import pyocr
import pyocr.builders
from open import openImg
import numpy as np
import glob

path_tesseract = 'C:\\Program Files\\Tesseract-OCR'
if path_tesseract not in os.environ['PATH'].split(os.pathsep):
  os.environ['PATH'] += os.pathsep + path_tesseract

tools = pyocr.get_available_tools()
tool = tools[0]

builder1 = pyocr.builders.DigitBuilder(tesseract_layout=6)

builder2 = pyocr.builders.DigitBuilder(tesseract_layout=7)

builder3 = pyocr.builders.TextBuilder(tesseract_layout=6)
builder3.tesseract_configs.append('-c')
builder3.tesseract_configs.append('tessedit_char_whitelist="0123456789"')

builder4 = pyocr.builders.TextBuilder(tesseract_layout=7)
builder4.tesseract_configs.append('-c')
builder4.tesseract_configs.append('tessedit_char_whitelist="0123456789"')

builder5 = pyocr.builders.TextBuilder(tesseract_layout=6)

builder6 = pyocr.builders.TextBuilder(tesseract_layout=7)

judges = ['PERFECT', 'GREAT', 'GOOD', 'BAD', 'MISS']
nums = ['0','1','2','3','4','5','6','7','8','9']
search_content = cv2.cvtColor(cv2.imread('./lib/template.png'), cv2.COLOR_BGR2RGB)
border = 230
WHITE = [255,255,255]

def judge(url):
  search_target = np.array(openImg(url))

  res = get_point(face_img=search_content, full_img=search_target)
  point = res['number']

  img = search_target[
    point['top'] : point['bottom'],
    point['left'] : point['right']
  ]

  datas = {}
  hight = img.shape[0] // 5

  for k in range(1,7):
    datas['builder' + str(k)] = {}

  for i in range(len(judges)):
    cropped_img = img[hight * i : hight * (i + 1), 0 : img.shape[1]]

    for y in range(cropped_img.shape[0]):
      for x in range(cropped_img.shape[1]):
        r, g, b = cropped_img[y][x]

        if r >= border and g >= border and b >= border:
          a = 0
        else:
          a = 255
        cropped_img[y][x][0] = a
        cropped_img[y][x][1] = a
        cropped_img[y][x][2] = a

    cropped_img = cv2.copyMakeBorder(cropped_img, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=WHITE)  

    for j in range(1,7):
      result = tool.image_to_string(Image.fromarray(cropped_img), lang='eng', builder=eval('builder' + str(j)))
      datas['builder' + str(j)][judges[i]] = result

  return datas

if __name__ == '__main__':
  result = judge('https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/normal.png')
  print(result)