import os
from PIL import Image
import pyocr
import pyocr.builders
import requests
import io
import matplotlib.pyplot as plt
import cv2
import numpy as np
from ratio import get_ratio
from IPython.display import display
from matplotlib import pyplot as plt
import math

# search_content == face_img
# search_target == full_img

# search_contentとsearch_targetはRGBのNumpyArray
def do_matching(search_content, search_target):
  color_range = 25

  # 上 1/2
  # 下 1/8
  # 右 1/4
  # 左 0
  # を切り取っている
  search_target = search_target[
    search_target.shape[0] // 2 : search_target.shape[0] // 8 * 7,
    0 : search_target.shape[1] // 4 * 3
  ]

  print(search_target.shape)

  if search_target.shape[0] <= search_content.shape[0]:
    ratio = 1 - (search_content.shape[0] - search_target.shape[0]) / search_content.shape[0]
  else:
    ratio = 1
  search_content = cv2.resize(search_content, None, None, ratio, ratio)

  search_target_ratio = get_ratio(search_content=search_content, search_target=search_target)['search_target']

  search_target = cv2.resize(search_target, None, None, search_target_ratio, search_target_ratio)

  result = cv2.matchTemplate(search_target, search_content, getattr(cv2, 'TM_CCOEFF_NORMED'))
  minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)

  tl = maxLoc
  br = (tl[0] + search_content.shape[1], tl[1] + search_content.shape[0])

  dst = search_target.copy()
  dst = dst[
    tl[1] + search_content.shape[0] // 10 * 3 - 5 : tl[1] + search_content.shape[0] // 10 * 3 + 5,
    tl[0] : dst.shape[1]
  ]

  np_dst = np.full((dst.shape[0], dst.shape[1]), 0)

  for y in range(dst.shape[0]):
    for x in range(dst.shape[1]):
      r, g, b = dst[y][x]

      if r<=70 and 215 <= g <= 255 and 205<=b<=236:
          a = 0
      elif 114-color_range < r < 144+color_range and 241-color_range < g < 241+color_range and 219-color_range < b < 219+color_range:
          a = 0
      elif 108-color_range < r < 108+color_range and 193-color_range < g < 193+color_range and 190-color_range < b < 190+color_range:
          a = 0
      elif 115-color_range < r < 115+color_range and 233-color_range < g < 233+color_range and 215-color_range < b < 215+color_range:
          a = 0
      else:
          a = 255
      
      np_dst[y][x] = a

  bb = False
  result2 = []

  for x in range(np_dst.shape[1]):
    bb = False
    for y in range(np_dst.shape[0]):
      if np_dst[y][x] == 0:
        bb = True
      else:
        bb = False
        break
    if bb:
      result2.append(x)
    
  # ToDo: 画像を縮小・拡大・クロップしたところを戻した座標を

  cv2.rectangle(search_target, tl, br, 255, 10)
  Image.fromarray(search_target).show()

  return result2, tl, br
  
if __name__ == '__main__':
  search_content = cv2.cvtColor(cv2.imread('./final/img2.png'), cv2.COLOR_BGR2RGB)
  search_target = cv2.cvtColor(cv2.imread('./targets/target.jpg'), cv2.COLOR_BGR2RGB)

  print(do_matching(search_content=search_content, search_target=search_target))