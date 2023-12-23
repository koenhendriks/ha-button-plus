"""Button+ connects several devices."""
from __future__ import annotations

import asyncio
import logging
import random
from typing import Callable

from .button_plus_api.local_api_client import LocalApiClient
from .button_plus_api.model import DeviceConfiguration
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client


_LOGGER: logging.Logger = logging.getLogger(__package__)


class ButtonPlusHub:
    """hub for Button+ example."""

    identifier = "button_plus_hub"
    manufacturer = "Button+"

    def __init__(self, hass: HomeAssistant, config: DeviceConfiguration) -> None:
        _LOGGER.debug(f"New hub with config {config.core}")
        self._hass = hass
        self._config = config
        self._name = config.core.name
        self._id = config.info.device_id
        self._client = LocalApiClient(config.info.ip_address, aiohttp_client.async_get_clientsession(hass))
        self.online = True
        self.devices = []
        self.devices.append(ButtonPlusBase(config, self))

    @property
    def client(self) -> LocalApiClient:
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

    def __init__(self, config: DeviceConfiguration, hub: ButtonPlusHub) -> None:
        """Init dummy button_plus_base."""
        self._id = config.info.device_id
        self.hub = hub
        self._config = config
        self.name = config.core.name
        self._callbacks = set()
        self._loop = asyncio.get_event_loop()
        self._target_position = 100
        self._current_position = 100

        self.firmware_version = config.info.firmware
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
