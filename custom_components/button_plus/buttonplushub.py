"""Button+ connects several devices."""

from __future__ import annotations

import logging
from typing import List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers import device_registry as DeviceRegistry
from homeassistant.helpers.device_registry import DeviceEntry

from .button_plus_api.connector_type import ConnectorType
from .button_plus_api.local_api_client import LocalApiClient
from .button_plus_api.model_interface import DeviceConfiguration
from .const import DOMAIN, MANUFACTURER

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ButtonPlusHub:
    """hub for Button+."""

    def __init__(
        self, hass: HomeAssistant, config: DeviceConfiguration, entry: ConfigEntry
    ) -> None:
        _LOGGER.debug(f"New hub with config {config}")
        self._hass = hass
        self.config = config
        self._name = config.name()
        self.identifier = config.identifier()
        self._client = LocalApiClient(
            config.ip_address(), aiohttp_client.async_get_clientsession(hass)
        )
        self.online = True
        self.button_entities = {}
        self.label_entities = {}
        self.top_label_entities = {}
        self.brightness_entities = {}

        self.manufacturer = MANUFACTURER
        self.model = "Base Module"

        device_registry = DeviceRegistry.async_get(hass)

        self.device = device_registry.async_get_or_create(
            configuration_url=f"http://{self.config.ip_address()}/",
            config_entry_id=entry.entry_id,
            connections={
                (DeviceRegistry.CONNECTION_NETWORK_MAC, self.config.mac_address())
            },
            identifiers={(DOMAIN, self.config.identifier())},
            manufacturer=self.manufacturer,
            suggested_area=self.config.location(),
            name=self._name,
            model=self.model,
            sw_version=str(config.firmware_version()),
        )

        # 1 or none display module
        self.display_module = next(
            (
                self.create_display_module(hass, entry, self)
                for _ in ButtonPlusHub.connector_identifiers_for(ConnectorType.DISPLAY, self)
            ),
            None,
        )
        self.display_bar = [
            (connector_id, self.create_bar_module(hass, entry, self, connector_id))
            for connector_id in ButtonPlusHub.connector_identifiers_for(ConnectorType.BAR, self)
        ]

        _LOGGER.info(f"Hub {self._name} created with {len(self.display_bar)} bar modules")

    @staticmethod
    def create_display_module(
        hass: HomeAssistant, entry: ConfigEntry, hub: ButtonPlusHub
    ) -> DeviceEntry:
        _LOGGER.warning(f"Create display module from {hub.hub_id}")
        device_registry = DeviceRegistry.async_get(hass)

        device = device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            #connections={(DOMAIN, hub.config.identifier())},
            name=f"{hub.name} Display Module",
            model="Display Module",
            manufacturer=MANUFACTURER,
            suggested_area=hub.config.location(),
            identifiers={(DOMAIN, f"{hub.hub_id} Display Module")},
            via_device=(DOMAIN, hub.hub_id),
        )

        return device

    @staticmethod
    def create_bar_module(
        hass: HomeAssistant,
        entry: ConfigEntry,
        hub: ButtonPlusHub,
        connector_id: int,
    ) -> DeviceEntry:
        _LOGGER.warning(f"Create bar module from {hub.hub_id} with connector '{connector_id}'")
        device_registry = DeviceRegistry.async_get(hass)

        device = device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            #connections={(DOMAIN, hub.config.identifier())},
            name=f"{hub._name} BAR Module {connector_id}",
            model="Bar module",
            manufacturer=MANUFACTURER,
            suggested_area=hub.config.location(),
            identifiers={(DOMAIN, f"{hub.hub_id} BAR Module {connector_id}")},
            via_device=(DOMAIN, hub.hub_id),
        )

        return device

    @staticmethod
    def connector_identifiers_for(connector_type: ConnectorType, hub: ButtonPlusHub) -> List[int]:
        return [
            connector.identifier()
            for connector in hub.config.connectors_for(connector_type)
        ]

    @property
    def client(self) -> LocalApiClient:
        """Return Button+ API client"""
        return self._client

    @property
    def hub_id(self) -> str:
        return self.identifier

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
