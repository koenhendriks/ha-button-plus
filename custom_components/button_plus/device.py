from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from custom_components.button_plus.buttonplushub import ButtonPlusHub

from .const import DOMAIN, MANUFACTURER


class BarModuleDevice:
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, hub: ButtonPlusHub, connector_id: int) -> None:
        self.device_registry = dr.async_get(hass)

        self.device = self.device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            connections={(DOMAIN, hub.config.info.device_id)},
            name=f"{hub._name} BAR Module {connector_id}",
            model="Bar module",
            manufacturer=MANUFACTURER,
            suggested_area=hub.config.core.location,
            identifiers={
                (DOMAIN, f"{hub._hub_id} BAR Module {connector_id}")
            },
            via_device=(DOMAIN, hub.hub_id)
        )

class DisplayModuleDevice:
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, hub: ButtonPlusHub) -> None:
        self.device_registry = dr.async_get(hass)

        self.device = self.device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            connections={(DOMAIN, hub.config.info.device_id)},
            name=f"{hub._name} Display Module",
            model="Display Module",
            manufacturer=MANUFACTURER,
            suggested_area=hub.config.core.location,
            identifiers={
                (DOMAIN, f"{hub._hub_id} Display Module")
            },
            via_device=(DOMAIN, hub.hub_id)
        )

