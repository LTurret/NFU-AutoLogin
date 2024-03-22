from asyncio import create_task
from asyncio import wait
from asyncio import new_event_loop
from asyncio import set_event_loop
from asyncio import FIRST_COMPLETED
from base64 import b64decode
from os import getenv
from os import path
from os import sep
from pickle import load
from re import findall
from re import search
from time import perf_counter

from dotenv import load_dotenv
from easyocr import Reader
from requests import get
from requests import post
from requests import Response

from validator import validator

load_dotenv()


async def login(reader: Reader) -> str:
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

    result: str = reader.readtext(b64decode(uri))

    if len(result) > 0:
        captchaCode: str = result[0][-2].replace(" ", "")
    else:
        return "captchaCode detect failed."

    # Build headers
    headers: dict = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    # Build POST data
    data: dict = {
        "username": getenv("nfu_username"),
        "password": getenv("nfu_password"),
        "captchaCode": captchaCode,
        "captchaKey": captchaKey,
    }

    # Send POST-request to login
    response: Response = post(url, headers=headers, data=data, cookies=cookies)

    # Check if we're login successfully
    if findall(r"firstChildTeachingClassesPage", response.text):
        for cookie in response.cookies:
            return cookie.value
    else:
        return "Login failed."


async def main():
    model: str = rf"{path.dirname(path.realpath(__file__))}{sep}model.pkl"

    # Validates require files.
    validator((getenv("nfu_username"), getenv("nfu_password")), model)

    with open(model, "rb") as model:
        reader: Reader = load(model)

    tasks: list = [create_task(login(reader)) for _ in range(7)]

    tpc: float = perf_counter()
    done, pending = await wait(tasks, return_when=FIRST_COMPLETED)

    for task in pending:
        task.cancel()

    for task in done:
        result = task.result()
        if result != "Login failed.":
            print(f"Login completed.\n{result}\n")
            timeup = perf_counter() - tpc
            print(f"{__file__} executed in {timeup:0.2f} seconds.")
            print("Now you can replace your session cookie with: https://ulearn.nfu.edu.tw")
            break


if __name__ == "__main__":
    loop = new_event_loop()
    set_event_loop(loop)
    loop.run_until_complete(main())
