from pydantic import BaseModel
from typing import Union


class Img(BaseModel):
    img: Union[str, bytes]


class ImgUrl(BaseModel):
    img: str


class ImgBytes(BaseModel):
    img: bytes
