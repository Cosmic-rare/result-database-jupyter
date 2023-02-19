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
import difflib
import json

path_tesseract = "C:\\Program Files\\Tesseract-OCR"
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract

tools = pyocr.get_available_tools()
tool = tools[0]

def getDifficult(musicId, difficult):
    with open('./json/difficult.json', encoding="utf-8") as f1:
        difficulties = json.load(f1)

        data = "n/a"

        for i in difficulties:
            if i["musicId"] == musicId and difficult.lower() == i["musicDifficulty"]:
                data = (i)

        return data

def check(target, musicId):
    difficults = ["EASY","NORMAL","HARD","EXPERT","MASTER"]

    data = {"credibility":0,"musicDifficulty":""}

    for j in difficults:
        result = difflib.SequenceMatcher(None, target, j).ratio()

        if result > data["credibility"]:
            data["musicDifficulty"] = j
            data["credibility"] = result

    data["ocr"] = target

    data["data"] = getDifficult(musicId, data["musicDifficulty"])

    return data

def difficult(url, musicId):
    img = Image.open(io.BytesIO(requests.get(url).content))    
    rgb_img = img.convert('RGB')
    size = rgb_img.size

    crop_img = rgb_img.crop([0, 0, size[0]/2, size[1]/7])
    crop_size = crop_img.size

    resize_img = crop_img.resize((math.floor(crop_size[0]/15), math.floor(crop_size[1]/15)))
    
    img2 = Image.new('RGBA',crop_size)

    for x in range(crop_size[0]):
        for y in range(crop_size[1]):
            r,g,b = crop_img.getpixel((x,y))

            if 94<r<175 and 179<g<255 and 28<b<108:
                a = 0
            elif 54<r<134 and 144<g<224 and 192<b<255:
                a = 0
            elif 204<r<255 and 135<g<215 and 21<b< 101:
                a = 0
            elif 180<r<255 and 42<g<122 and 64<b<144:
                a = 0
            elif 132<r<212 and 22<g<102 and 190<b<255:
                a = 0
            else:
                a = 255

            img2.putpixel((x,y),(a,a,a,255))
    
    builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    builder.tesseract_configs.append("-c")
    builder.tesseract_configs.append("tessedit_char_whitelist=\"EASYNORMLHDXPT\"")
    data = tool.image_to_string(img2, lang="eng", builder=builder)
    
    return check(data, musicId)