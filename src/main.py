from os import getenv
from re import findall
from re import search

from dotenv import load_dotenv
from requests import get
from requests import post
from requests import Response

load_dotenv()


def login(username: str, password: str) -> None:
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
    uri: str = search(r"(data:image\/png;base64,.+)\",", callback.text).group(1)
    ocr_api: str = "https://api.ocr.space/parse/image"
    data: dict = {"apikey": "K89764407788957", "base64Image": uri, "language": "eng", "OCREngine": 3}
    response: Response = post(ocr_api, data=data)

    try:
        result: str = response.text
        result = search(r"LineText\":\"(.+)\",\"Words", result).group(1)
        captchaCode: str = result.replace(" ", "")
    except:
        raise Exception("Captcha detect failed")

    # Build headers
    headers: dict = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    # Build POST data
    data: dict = {
        "username": username,
        "password": password,
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
        raise Exception("Login failed, due to wrong captcha code")


if __name__ == "__main__":
    username: str = getenv("nfu_username")
    password: str = getenv("nfu_password")

    assert username is not None, '"nfu_username" variable not found, did you place your secrets in ".env" correctly?'
    assert password is not None, '"nfu_password" variable not found, did you place your secrets in ".env" correctly?'

    print("Login attemping...")

    while True:
        try:
            login(username, password)
            input("Complete, type anything to exit!\n")
            break
        except Exception as exception:
            print(f"{exception}, Retrying...")
            pass
