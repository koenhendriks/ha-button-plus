from __future__ import annotations

import json
import re
import logging

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ApiClient:
    """Client to talk to Button+ website"""

    def __init__(self, session, cookie=None) -> None:
        _LOGGER.debug(f"DEBUG CONFIG {cookie}")
        self._base = "https://api.button.plus"
        self._session = session

        if not cookie:
            cookie = ""

        self._cookie = cookie
        self._headers = {
            "authority": "api.button.plus",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-NL,en-US;q=0.9,en;q=0.8,nl-NL;q=0.7,nl;q=0.6,en-GB;q=0.5",
            "cache-control": "no-cache",
            "cookie": self._cookie,
        }

        _LOGGER.debug("Initialize Button+ API client")

    async def test_connection(self):
        url = f"{self._base}/button/buttons"
        _LOGGER.debug(f"test_connection on {url}")
        async with self._session.get(url, headers=self._headers) as response:
            _LOGGER.debug(f"Fetch website validation = {response.status} {response}")
            return 200 <= response.status < 300

    async def fetch_config(self, config=int):
        url = f"{self._base}/button/config/{config}"
        _LOGGER.debug(f"fetch_config {url}")
        async with self._session.get(url, headers=self._headers) as response:
            return await response.text()

    async def fetch_configs(self):
        url = f"{self._base}/button/buttons"
        _LOGGER.debug(f"fetch_configs {url}")
        async with self._session.get(url, headers=self._headers) as response:
            return await response.text()

    async def get_cookie_from_login(self, email=str, password=str):
        url = f"{self._base}/account/login"
        data = {"email": email, "password": password, "remember": True}
        json_data = json.dumps(data)
        _LOGGER.debug(f"json dump: {json_data}")
        headers = {
            "accept": "*/*",
            "accept-language": "en-NL,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://button.plus",
            "referer": "https://button.plus/",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }

        async with self._session.post(url, data=json_data, headers=headers) as response:
            response_body = await response.text()

            if not response.cookies:
                raise Exception(
                    f"Login error with username and password, response: {response_body}"
                )

            cookie_string = str(response.cookies)
            match = re.search(r"auth_cookie=[^;]+", cookie_string)

            auth_cookie = match.group()

            return auth_cookie
