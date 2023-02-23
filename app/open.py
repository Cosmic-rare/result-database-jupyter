from PIL import Image
import requests
import io

def openImg(url):
    return Image.open(io.BytesIO(requests.get(url).content))
