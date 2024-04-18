from base64 import b64decode
from re import search

from requests import get
from requests import Response

from easyocr import Reader


def gatherKey() -> str:
    api: str = "https://identity.nfu.edu.tw/auth/realms/nfu/captcha/code"
    callback: Response = get(api)
    return callback


def solver(reader: Reader, uri: str) -> str:
    result: list[str] = reader.readtext(b64decode(uri))
    print(result)

    if not len(result):
        raise ValueError("Solve failed.")

    captchaCode: str = result[0][-2].replace(" ", "")
    return captchaCode
