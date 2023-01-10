import requests
import io
from flask import current_app
from io import BytesIO
import os
from PIL import Image
from github import Github

from base64 import b64encode


def saveImg(productImage, imageFilename):
    g = Github(os.environ.get("GITT"))
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
    i.save(os.path.join(os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
            ), 'static'
        ), imageFilename))
    print(os.path.abspath(imageFilename))
