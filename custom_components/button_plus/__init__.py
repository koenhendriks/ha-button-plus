"""The Button+ integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.button_plus.button_plus_api.model_interface import DeviceConfiguration
from custom_components.button_plus.button_plus_api.model_detection import ModelDetection
from custom_components.button_plus.buttonplushub import ButtonPlusHub
from custom_components.button_plus.const import DOMAIN
from custom_components.button_plus.coordinator import ButtonPlusCoordinator


_LOGGER = logging.getLogger(__name__)

# List of platforms to support. There should be a matching .py file for each,
# eg <cover.py> and <sensor.py>
PLATFORMS: list[str] = ["button", "text", "number"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Button+ from a config entry."""
    _LOGGER.debug(f"Button+ init got new device entry! {entry.entry_id.title}")
    device_configuration: DeviceConfiguration = ModelDetection.model_for_json(
        entry.data.get("config")
    )

    hub = ButtonPlusHub(hass, device_configuration, entry)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = hub

    buttonplus_coordinator = ButtonPlusCoordinator(hass, hub)

    await buttonplus_coordinator.async_config_entry_first_refresh()

    # This creates each HA object for each platform your device requires.
    # It's done by calling the `async_setup_entry` function in each platform module.

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # This is called when an entry/configured device is to be removed. The class
    # needs to unload itself, and remove callbacks. See the classes for further
    # details
    _LOGGER.debug("Removing async_unload_entry")
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
