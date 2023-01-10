import requests
import io
from io import BytesIO

from PIL import Image

import base64


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
    resp_img = BytesIO(resp.content)
    img = Image.open(resp_img)
    img.save(resp_img, "PNG")
    base64img = "data:image/png;base64,"+b64encode(resp_img.getvalue()).decode('ascii')
    return base64img
