from __future__ import annotations

import logging

import aiohttp

_LOGGER: logging.Logger = logging.getLogger(__package__)


class LocalApiClient:
    """ Client to talk to Button+ local devices """

    def __init__(self, ip_address, session) -> None:
        self._base = f"http://{ip_address}"
        self._session = session

        _LOGGER.debug(f"Initialize Button+ local API client")

    async def fetch_config(self, config=int):
        url = f"{self._base}/config"
        _LOGGER.debug(f"fetch_config {url}")
        async with self._session.get(url) as response:
            return await response.text()
