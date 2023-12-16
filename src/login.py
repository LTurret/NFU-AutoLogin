from base64 import b64decode
from os import getenv
from os import sep
from re import findall
from re import search

from cv2 import cvtColor
from cv2 import imread
from cv2 import COLOR_BGR2RGB
from dotenv import load_dotenv
from easyocr import Reader
from requests import get
from requests import post
from requests import Response

load_dotenv()


def login(reader: Reader):
    # Make a base request to get essentials
    url: str = "https://identity.nfu.edu.tw/auth/realms/nfu/protocol/cas/login?service=https://ulearn.nfu.edu.tw/login"
    response: Response = get(url)

    # Fetch cookies
    cookies: dict = dict(response.cookies)

    # Fetch login url
    url: str = search(r'action="(\S+)"', response.text).group(1).replace("&amp;", "&")

    # Fetch valid captchaKey
    api: str = "https://identity.nfu.edu.tw/auth/realms/nfu/captcha/code"
    callback: Response = get(api)
    captchaKey: str = search(r"\"key\":\"(.+)\"", callback.text).group(1)

    # Breaking captchaCode
    uri: str = search(r"data:image\/png;base64,(.+)\",\"", callback.text).group(1)

    with open(f".{sep}captcha.png", "wb") as file:
        file.write(b64decode(uri))

    img = imread(f".{sep}captcha.png")
    img = cvtColor(img, COLOR_BGR2RGB)

    result = reader.readtext(img)

    if len(result) > 0:
        captchaCode: str = result[0][-2].replace(" ", "")
    else:
        raise "captchaCode detect failed."

    # Build headers
    headers: dict = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    # Build POST data
    data: dict = {
        "username": getenv("username"),
        "password": getenv("password"),
        "captchaCode": captchaCode,
        "captchaKey": captchaKey,
    }

    # Send POST-request to login
    response: Response = post(url, headers=headers, data=data, cookies=cookies)

    # Check if we're login successfully
    if findall(r"firstChildTeachingClassesPage", response.text):
        print("login successfully")
        for cookie in response.cookies:
            print(cookie.value)
    else:
        raise "Login failed."
