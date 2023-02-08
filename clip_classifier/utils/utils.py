from PIL import Image
from io import BytesIO
import requests
from typing import Union


def load_image(img: Union[str, bytes]):
    if isinstance(img, str):
        return request_image(img)
    else:
        return read_raw_image(img)


def request_image(img_url):
    try:
        img = Image.open(requests.get(img_url, stream=True).raw)
        return img
    except Exception as e:
        print(e)
        print("image could not be opened")


def read_raw_image(image_bytes):
    return Image.open(BytesIO(image_bytes))


def expand_list(labels):
    if len(labels) == 1:
        labels = labels[0].split(',')
    return labels
