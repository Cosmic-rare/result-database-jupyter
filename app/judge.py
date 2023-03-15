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

path_tesseract = "C:\\Program Files\\Tesseract-OCR"
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract

tools = pyocr.get_available_tools()
tool = tools[0]

builder = pyocr.builders.DigitBuilder(tesseract_layout=7)
# builder.tesseract_configs.append("-c")
# builder.tesseract_configs.append('tessedit_char_whitelist="0123456789"')

judges = ['PERFECT', 'GREAT', 'GOOD', 'BAD', 'MISS']
search_content = cv2.cvtColor(cv2.imread('./lib/template.png'), cv2.COLOR_BGR2RGB)
border = 230
WHITE = [255,255,255]

def judge(url):
  search_target = np.array(openImg(url))

  res = get_point(face_img=search_content, full_img=search_target)
  point = res["number"]

  img = search_target[
    point['top'] : point['bottom'],
    point['left'] : point['right']
  ]

  datas = {}
  hight = img.shape[0] // 5

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
    datas[judges[i]] = tool.image_to_string(Image.fromarray(cropped_img), lang="eng", builder=builder)

  return datas

if __name__ == '__main__':
  result = judge('https://raw.githubusercontent.com/Cosmic-rare/result-database-jupyter/main/targets/normal.png')
  print(result)