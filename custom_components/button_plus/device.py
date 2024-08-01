from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from .buttonplushub import ButtonPlusHub, _LOGGER
from .const import DOMAIN, MANUFACTURER


class BarModuleDevice:
    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        hub: ButtonPlusHub,
        connector_id: int,
    ) -> None:
        _LOGGER.info(
            f"Init BarModuleDevice '{hub.hub_id}' with connector '{connector_id}'"
        )
        self.device_registry = dr.async_get(hass)
        self.device = self.device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            connections={(DOMAIN, hub.config.identifier())},
            name=f"{hub.name} BAR Module {connector_id}",
            model="Bar module",
            manufacturer=MANUFACTURER,
            suggested_area=hub.config.location(),
            identifiers={(DOMAIN, f"{hub.hub_id} BAR Module {connector_id}")},
            via_device=(DOMAIN, hub.hub_id),
        )


class DisplayModuleDevice:
    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, hub: ButtonPlusHub
    ) -> None:
        _LOGGER.info(f"Init DisplayModuleDevice {hub.hub_id}")
        self.device_registry = dr.async_get(hass)
        self.device = self.device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            connections={(DOMAIN, hub.config.identifier())},
            name=f"{hub.name} Display Module",
            model="Display Module",
            manufacturer=MANUFACTURER,
            suggested_area=hub.config.location(),
            identifiers={(DOMAIN, f"{hub.hub_id} Display Module")},
            via_device=(DOMAIN, hub.hub_id),
        )
