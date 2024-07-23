"""Button+ connects several devices."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client

from .button_plus_api.local_api_client import LocalApiClient
from .button_plus_api.connector_type import ConnectorEnum
from .button_plus_api.model_interface import DeviceConfiguration
from .const import DOMAIN, MANUFACTURER


_LOGGER: logging.Logger = logging.getLogger(__package__)


class ButtonPlusHub:
    """hub for Button+."""

    def __init__(
        self, hass: HomeAssistant, config: DeviceConfiguration, entry: ConfigEntry
    ) -> None:
        _LOGGER.debug(f"New hub with config {config.core}")
        self._hass = hass
        self.config = config
        self._name = config.core.name or config.info.device_id
        self._id = config.info.device_id
        self._client = LocalApiClient(
            config.info.ip_address, aiohttp_client.async_get_clientsession(hass)
        )
        self.online = True
        self.button_entities = {}
        self.label_entities = {}
        self.top_label_entities = {}
        self.brightness_entities = {}

        device_registry = dr.async_get(hass)

        self.device = device_registry.async_get_or_create(
            configuration_url=f"http://{self.config.info.ip_address}/",
            config_entry_id=entry.entry_id,
            connections={(dr.CONNECTION_NETWORK_MAC, self.config.info.mac)},
            identifiers={(DOMAIN, self.config.info.device_id)},
            manufacturer=MANUFACTURER,
            suggested_area=self.config.core.location,
            name=self._name,
            model="Base Module",
            sw_version=config.info.firmware,
        )

        # 1 or none display module
        self.display_module = next(
            (
                self.create_display_module(hass, entry, self)
                for _ in self.connector(ConnectorEnum.DISPLAY)
            ),
            None,
        )
        self.display_bar = [
            (connector_id, self.create_bar_module(hass, entry, self, connector_id))
            for connector_id in self.connector(ConnectorEnum.BAR)
        ]

    def create_display_module(
        self, hass: HomeAssistant, entry: ConfigEntry, hub: ButtonPlusHub
    ) -> None:
        _LOGGER.debug(f"Add display module from '{hub.hub_id}'")
        device_registry = dr.async_get(hass)

        device = device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            # connections={(DOMAIN, hub.config.info.device_id)},
            name=f"{hub.name} Display Module",
            model="Display Module",
            manufacturer=MANUFACTURER,
            suggested_area=hub.config.core.location,
            identifiers={(DOMAIN, f"{hub.hub_id} Display Module")},
            via_device=(DOMAIN, hub.hub_id),
        )

        return device

    def create_bar_module(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        hub: ButtonPlusHub,
        connector_id: int,
    ) -> None:
        _LOGGER.debug(
            f"Add bar module from '{hub.hub_id}' with connector '{connector_id}'"
        )
        device_registry = dr.async_get(hass)

        device = device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            # connections={(DOMAIN, hub.config.info.device_id)},
            name=f"{hub._name} BAR Module {connector_id}",
            model="Bar module",
            manufacturer=MANUFACTURER,
            suggested_area=hub.config.core.location,
            identifiers={(DOMAIN, f"{hub.hub_id} BAR Module {connector_id}")},
            via_device=(DOMAIN, hub.hub_id),
        )

        return device

    def connector(self, connector_type: ConnectorEnum):
        return [
            connector.connector_id
            for connector in self.config.info.connectors
            if connector.connector_type_enum() in [connector_type]
        ]

    @property
    def client(self) -> LocalApiClient:
        """Return Button+ API client"""
        return self._client

    @property
    def hub_id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    def add_button(self, button_id, entity):
        self.button_entities[str(button_id)] = entity

    def add_label(self, button_id, entity):
        self.label_entities[str(button_id)] = entity

    def add_top_label(self, button_id, entity):
        self.top_label_entities[str(button_id)] = entity

    def add_brightness(self, identifier, entity):
        self.brightness_entities[identifier] = entity
