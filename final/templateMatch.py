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
import math

def match(face_img, full_img):
  # 2つの画像をマッチングする
  result = cv2.matchTemplate(full_img, face_img, cv2.TM_CCOEFF_NORMED)
  minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)

  tl = maxLoc
  br = (tl[0] + face_img.shape[1], tl[1] + face_img.shape[0])

  return tl, br

def grayscale(dst, color_range):
  # 例の青緑色を黒,それ以外を白にして出力する
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
  
  return np_dst

def black_line(np_dst, search_target_ratio):
  # 縦のすべての列が黒の地点のx座標を調べる
  result = []

  for x in range(np_dst.shape[1]):
    b = False
    for y in range(np_dst.shape[0]):
      if np_dst[y][x] == 0:
        b = True
      else:
        # 白なら抜ける
        break
    if b:
      # 縦すべてが黒の時
      result.append(math.floor((1 / search_target_ratio) * x))

  return result

class Ratio:
  def __init__(self, ratio, full_hight, tl, br):
    self.ratio = ratio
    self.hight = full_hight // 2
    self.top = self.restore(tl[1]) + self.hight
    self.bottom = self.restore(br[1]) + self.hight
  
  def restore(self, num):
    return math.floor(num * self.ratio)

def get_point(face_img, full_img):
  full_img_shape = full_img.shape

  # 変なところに特徴点がプロットされないように,なるべく小さくしておく
  full_img = full_img[
    full_img.shape[0] // 2 : full_img.shape[0] // 8 * 7,
    0 : full_img.shape[1] // 4 * 3
  ]

  # 検索内容が全体より大きくならないように縮小
  if full_img.shape[0] <= face_img.shape[0]:
    search_content_ratio = 1 - (face_img.shape[0] - full_img.shape[0]) / face_img.shape[0]
  else:
    search_content_ratio = 1
  face_img = cv2.resize(face_img, None, None, search_content_ratio, search_content_ratio)

  # DPIを揃えるための比と,戻すための比
  search_target_ratio = get_ratio(search_content=face_img, search_target=full_img)['search_target']
  full_ratio = 1 / search_target_ratio

  # DPIを揃える
  full_img = cv2.resize(full_img, None, None, search_target_ratio, search_target_ratio)

  # マッチングをする
  tl, br = match(face_img=face_img, full_img=full_img)

  # 緑線検出をする(crop -> grayscale -> get_position)
  dst = full_img.copy()
  dst = dst[
    tl[1] + face_img.shape[0] // 10 * 3 - 5 : tl[1] + face_img.shape[0] // 10 * 3 + 5,
    tl[0] : dst.shape[1]
  ]
  np_dst = grayscale(dst=dst, color_range=25)
  result = black_line(np_dst=np_dst, search_target_ratio=search_target_ratio)

  # 拡大を戻すいろいろ
  a = Ratio(ratio=full_ratio, full_hight=full_img_shape[0], tl=tl, br=br)

  # crop,search_target_ratioを配慮して座標を計算する
  final = {
    "character": {
      "top": a.top, "bottom": a.bottom, "left": a.restore(tl[0]), "right": a.restore(br[0])
    },
    "both": {
      "top": a.top, "bottom": a.bottom, "left": a.restore(tl[0]), "right": a.restore(tl[0]) + result[0] - 5
    },
    "number": {
      "top": a.top, "bottom": a.bottom, "left": a.restore(br[0]), "right": a.restore(tl[0]) + result[0] - 5
    }
  }

  return final
  
if __name__ == '__main__':
  search_content = cv2.cvtColor(cv2.imread('./final/img2.png'), cv2.COLOR_BGR2RGB)
  search_target = cv2.cvtColor(cv2.imread('./targets/normal.png'), cv2.COLOR_BGR2RGB)

  res = get_point(face_img=search_content, full_img=search_target)
  point = res["number"]

  cv2.rectangle(search_target, (point["left"], point["top"]), (point["right"], point["bottom"]), 255, 4)
  Image.fromarray(search_target).show()