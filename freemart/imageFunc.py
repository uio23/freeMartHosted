import requests

from io import io, BytesIO

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
    img = Image.open(BytesIO(resp.content))
    data = io.BytesIO()
    img.save(data, format="PNG")
    encoded_img_data = base64.b64encode(data.getvalue())
    return encoded_img_data
