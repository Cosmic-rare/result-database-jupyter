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
def do_matching(face_img, full_img):
  full_img = full_img[
    full_img.shape[0] // 2 : full_img.shape[0] // 8 * 7,
    0 : full_img.shape[1] // 4 * 3
  ]

  full_img2 = full_img.copy()

  if full_img.shape[0] <= face_img.shape[0]:
    ratio = 1 - (face_img.shape[0] - full_img.shape[0]) / face_img.shape[0]
  else:
    ratio = 1

  face_img = cv2.resize(face_img, None, None, ratio, ratio)

  search_target_ratio = get_ratio(search_content=face_img, search_target=full_img)['search_target']

  full_img = cv2.resize(full_img, None, None, search_target_ratio, search_target_ratio)

  result = cv2.matchTemplate(full_img, face_img, cv2.TM_CCOEFF_NORMED)
  minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)

  tl = maxLoc
  br = (tl[0] + face_img.shape[1], tl[1] + face_img.shape[0])

  dst = full_img.copy()

  dst = dst[
    tl[1] + face_img.shape[0] // 10 * 3 - 5 : tl[1] + face_img.shape[0] // 10 * 3 + 5,
    tl[0] : dst.shape[1]
  ]

  np_dst = np.full((dst.shape[0], dst.shape[1]), 0)
  color_range = 25

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

  result2 = []

  for x in range(np_dst.shape[1]):
    b = False
    for y in range(np_dst.shape[0]):
      if np_dst[y][x] == 0:
        b = True
      else:
        b = False
        break
    if b:
      result2.append(math.floor((1 / search_target_ratio) * x))

  full_ratio = 1 / search_target_ratio

  final = full_img2[
    math.floor(full_ratio * tl[1]) : math.floor(full_ratio * br[1]),
    math.floor(full_ratio * tl[0]) : math.floor(full_ratio * tl[0]) + result2[0] - 5
  ]

  return final
  
if __name__ == '__main__':
  search_content = cv2.cvtColor(cv2.imread('./final/img2.png'), cv2.COLOR_BGR2RGB)
  search_target = cv2.cvtColor(cv2.imread('./targets/normal.png'), cv2.COLOR_BGR2RGB)

  res = do_matching(face_img=search_content, full_img=search_target)

  Image.fromarray(res).show()