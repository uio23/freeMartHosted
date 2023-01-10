import requests
import io
from io import BytesIO
import os
from PIL import Image

from base64 import b64encode


def saveImg(productImage, imageFilename):
    img = Image.open(productImage)
    img = img.resize((500, 500))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    for repo in g.get_user().get_repos():
        if repo.name == "freemart_img":
            repo.create_file(imageFilename, "Img added", bytes(img_byte_arr), "main")
            return True
    return False


def loadImg(imageFilename):
    url = f'https://raw.githubusercontent.com/uio23/freemart_img/main/{imageFilename}'
    resp = requests.get(url)
    i = Image.open(BytesIO(resp.content))
    i.save(imageFilename)
    print(os.path.abspath(imageFilename))
