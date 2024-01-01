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

    async def fetch_config(self):
        url = f"{self._base}/config"
        _LOGGER.debug(f"fetch_config {url}")
        async with self._session.get(url) as response:
            return await response.text()

    async def push_config(self, config):
        url = f"{self._base}/configsave"
        _LOGGER.debug(f"push_config {url}")
        async with self._session.post(url, data=config.to_json()) as response:
            return await response.text()

