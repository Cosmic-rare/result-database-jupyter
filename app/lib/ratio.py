import math
import cv2
import matplotlib.pyplot as plt

def bubble_sort(arr):
  # ただのソート
  change = True
  while change:
    change = False
    for i in range(len(arr) - 1):
      if arr[i].distance > arr[i + 1].distance:
        arr[i].distance, arr[i + 1].distance = arr[i + 1].distance, arr[i].distance
        change = True
  return arr

def get_distance(x1, y1, x2, y2):
  # 二点間の距離を三平方の定理で求める
  d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
  return d

# search_contentとsearch_targetはRGBのNumpyArray
def get_ratio(search_content, search_target):
  # 特徴点の検出
  akaze = cv2.AKAZE_create()                                
  kp1, des1 = akaze.detectAndCompute(cv2.cvtColor(search_content,cv2.COLOR_BGR2GRAY) , None)
  kp2, des2 = akaze.detectAndCompute(cv2.cvtColor(search_target,cv2.COLOR_BGR2GRAY) , None)

  # 特徴点のマッチング
  bf = cv2.BFMatcher()
  matches = bf.knnMatch(des1, des2, k=2)

  # 特徴点の間引き
  ratio = 0.75
  good2 = []
  for m, n in matches:
    if m.distance < ratio * n.distance:
      good2.append(m)

  # 精度順にソートして、距離を求めて、倍率を出す
  good2 = bubble_sort(good2)

  distance_content = get_distance(
      x1=kp1[good2[0].queryIdx].pt[0],
      y1=kp1[good2[0].queryIdx].pt[1],
      x2=kp1[good2[1].queryIdx].pt[0],
      y2=kp1[good2[1].queryIdx].pt[1]
  )
  distance_target = get_distance(
      x1=kp2[good2[0].trainIdx].pt[0],
      y1=kp2[good2[0].trainIdx].pt[1],
      x2=kp2[good2[1].trainIdx].pt[0],
      y2=kp2[good2[1].trainIdx].pt[1]
  )

  # Magnification factor to match DPI
  return {'search_content': 1, 'search_target': 1 / (distance_target / distance_content)}

if __name__ == '__main__':
  search_content = cv2.cvtColor(cv2.imread('./final/img2.png'), cv2.COLOR_BGR2RGB)
  search_target = cv2.cvtColor(cv2.imread('./targets/wide.png'), cv2.COLOR_BGR2RGB)

  print(get_ratio(search_content=search_content, search_target=search_target))