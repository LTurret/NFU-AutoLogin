from http.cookies import Morsel
from re import search
from typing import Dict


async def fetch(session) -> dict:
    url: str = "https://identity.nfu.edu.tw/auth/realms/nfu/protocol/cas/login?service=https://ulearn.nfu.edu.tw/login"

    async with session.get(url) as response:
        cookies: Dict[str, Morsel] = session.cookie_jar.filter_cookies(url)
        respond: str = await response.text()

    login_url: str = search(r'action="(\S+)"', respond).group(1).replace("&amp;", "&")
    return {"login_url": login_url, "cookies": cookies}
