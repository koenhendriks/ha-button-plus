""" Button+ API client and utilities"""
from __future__ import annotations

import logging

import aiohttp

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ApiClient:
    """ Client to talk to Button+ device """

    def __init__(self, cookie=str) -> None:
        self._base = "https://api.button.plus"
        self._cookie = cookie
        self._headers = {
            'authority': 'api.button.plus',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-NL,en-US;q=0.9,en;q=0.8,nl-NL;q=0.7,nl;q=0.6,en-GB;q=0.5',
            'cache-control': 'no-cache',
            'cookie': self._cookie,
        }

        _LOGGER.debug(f"Initialize Button+ API client (NEW)")

    async def fetch_config(self, config=int):
        url = f"{self._base}/button/config/{config}"
        _LOGGER.debug(f"fetch_config {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers) as response:
                return await response.text()

    async def fetch_configs(self):
        url = f"{self._base}/button/buttons"
        _LOGGER.debug(f"fetch_configs {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers) as response:
                return await response.text()
