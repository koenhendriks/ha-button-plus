"""Button+ connects several devices."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr

from .button_plus_api.local_api_client import LocalApiClient
from .button_plus_api.model import DeviceConfiguration
from homeassistant.core import HomeAssistant
from .const import DOMAIN, MANUFACTURER
from homeassistant.helpers import aiohttp_client

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ButtonPlusHub:
    """hub for Button+."""

    def __init__(self, hass: HomeAssistant, config: DeviceConfiguration, entry: ConfigEntry) -> None:
        _LOGGER.debug(f"New hub with config {config.core}")
        self._hass = hass
        self.config = config
        self._name = config.info.device_id
        self._id = self.config.info.device_id
        self._client = LocalApiClient(config.info.ip_address, aiohttp_client.async_get_clientsession(hass))
        self.online = True
        self.button_entities = {}
        self.label_entities = {}
        self.top_label_entities = {}

        device_registry = dr.async_get(hass)

        device_registry.async_get_or_create(
            configuration_url=f"http://{self.config.info.ip_address}/",
            config_entry_id=entry.entry_id,
            connections={(dr.CONNECTION_NETWORK_MAC, self.config.info.mac)},
            identifiers={(DOMAIN, self.config.info.device_id)},
            manufacturer=MANUFACTURER,
            suggested_area=self.config.core.location,
            name=self._name,
            model="Base Module",
            hw_version=config.info.firmware
        )

    @property
    def client(self) -> LocalApiClient:
        """Return Button+ API client"""
        return self._client

    @property
    def hub_id(self) -> str:
        return self._id

    def add_button(self, button_id, entity):
        self.button_entities[str(button_id)] = entity

    def add_label(self, button_id, entity):
        self.label_entities[str(button_id)] = entity

    def add_top_label(self, button_id, entity):
        self.top_label_entities[str(button_id)] = entity
