from asyncio import create_task
from asyncio import gather
from asyncio import wait
from asyncio import new_event_loop
from asyncio import set_event_loop
from asyncio import AbstractEventLoop
from asyncio import Task
from asyncio import FIRST_COMPLETED
from base64 import b64decode
from http.cookies import Morsel
from os import getenv
from os import path
from os import sep
from pickle import load
from re import findall
from re import search
from time import perf_counter
from typing import Dict
from typing import List

from aiohttp import ClientSession
from dotenv import load_dotenv
from easyocr import Reader
from requests import get
from requests import Response

from validator import validator
from fetch_util import fetch

load_dotenv()


async def login(reader: Reader) -> str:
    async with ClientSession() as session:
        task: List[Task] = [create_task(fetch(session))]
        await gather(*task)
        login_url: str = task[0].result()["login_url"]
        cookies: Dict[str, Morsel] = task[0].result()["cookies"]

    # Fetch valid captchaKey
    api: str = "https://identity.nfu.edu.tw/auth/realms/nfu/captcha/code"
    callback: Response = get(api)
    captchaKey: str = search(r"\"key\":\"(.+)\"", callback.text).group(1)

    # Breaking captchaCode
    uri: str = search(r"data:image\/png;base64,(.+)\",\"", callback.text).group(1)
    result: List[str] = reader.readtext(b64decode(uri))

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
    async with ClientSession(cookies=cookies, headers=headers) as session:
        async with session.post(url=login_url, data=data) as response:
            respond: str = await response.text()
            cookies: Dict[str, Morsel] = session.cookie_jar.filter_cookies("https://ulearn.nfu.edu.tw/")

            if findall(r"firstChildTeachingClassesPage", respond):
                for _, cookie in cookies.items():
                    if cookie.key == "session":
                        return cookie.value
            else:
                return "Login failed."


async def main():
    model: str = rf"{path.dirname(path.realpath(__file__))}{sep}model.pkl"

    validator((getenv("nfu_username"), getenv("nfu_password")), model)

    with open(model, "rb") as model:
        reader: Reader = load(model)

    tasks: List[Task] = [create_task(login(reader)) for _ in range(7)]
    tpc: float = perf_counter()
    flag: bool = False

    while not flag:
        done, _ = await wait(tasks, return_when=FIRST_COMPLETED)

        for task in done:
            result = task.result()

            if result != "Login failed.":
                print(f"Login completed.\n{result}\n")
                timeup = perf_counter() - tpc
                print(f"completed with {timeup:0.2f} seconds.")
                print("Now you can replace your session cookie with: https://ulearn.nfu.edu.tw")
                flag = True


if __name__ == "__main__":
    loop: AbstractEventLoop = new_event_loop()
    set_event_loop(loop)
    loop.run_until_complete(main())
