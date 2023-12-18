"""Button+ connects several devices."""
from __future__ import annotations

import asyncio
import json
import logging
import random
from typing import Callable

from homeassistant.core import HomeAssistant

from .button_plus_api import ApiClient

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ButtonPlusHub:
    """hub for Button+ example."""

    identifier = "button_plus_hub"
    manufacturer = "Button+"

    def __init__(self, hass: HomeAssistant, cookie: str) -> None:
        self._hass = hass
        self._cookie = cookie
        self._name = self.identifier
        self._id = self.identifier
        self._client = ApiClient(cookie)
        self.online = False
        self.devices = []

    async def init(self):
        configs = await self._client.fetch_configs()
        data = json.loads(configs)
        _LOGGER.debug(f"Found configurations for Button+:")
        for index, config in enumerate(data):
            default_ip = f"Unknown IP {index}"
            default_name = f"No name {index}"
            _LOGGER.debug(
                f"ID: {config.get('Id')}, IP: {config.get('IpAddress')} Name: {config.get('Name')} ")

            self.devices.append(ButtonPlusBase(config.get('Id'), config.get('Name'), self))

        return self

    @property
    def client(self) -> ApiClient:
        """Return Button+ API client"""
        return self._client

    @property
    def hub_id(self) -> str:
        return self._id

    async def test_connection(self) -> bool:
        """Test connectivity to the ButtonPlus base is OK."""
        return True


class ButtonPlusBase:
    """ Button+ Base device"""

    def __init__(self, button_plus_base_id: str, name: str, hub: ButtonPlusHub) -> None:
        """Init dummy button_plus_base."""
        self._id = button_plus_base_id
        self.hub = hub
        self.name = name
        self._callbacks = set()
        self._loop = asyncio.get_event_loop()
        self._target_position = 100
        self._current_position = 100

        self.firmware_version = f"0.0.{random.randint(1, 9)}"
        self.model = "Base Module"

    @property
    def button_plus_base_id(self) -> str:
        """Return ID for button_plus_base."""
        return self._id

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register callback, called when button_plus_base changes state."""
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

    async def publish_updates(self) -> None:
        """Schedule call all registered callbacks."""
        for callback in self._callbacks:
            callback()

    @property
    def online(self) -> float:
        """button_plus_base is online."""
        return True

    @property
    def illuminance(self) -> int:
        """Return a value for illuminance sensor."""
        return random.randint(0, 500)
