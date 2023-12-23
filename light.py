""" Platform for light integration. """
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.light import LightEntity, ColorMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import ButtonPlusHub

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

lights = []


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Add switches for passed config_entry in HA."""

    hub: ButtonPlusHub = hass.data[DOMAIN][config_entry.entry_id]
    buttons = hub.config.mqtt_buttons

    for button in buttons:
        lights.append(ButtonPlusLight(button.button_id, button.label, hub.hub_id))

    async_add_entities(lights)


class ButtonPlusLight(LightEntity):
    def __init__(self, btn_id, btn_label, hub_id):
        self._attr_unique_id = f'light-{hub_id}-{btn_id}'
        self._hub_id = hub_id
        self._attr_name = f'light-{btn_id}'
        self._name = btn_label
        self._state = False

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        # Need to apply mqtt logic here to see if its on
        return self._state

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Instruct the light to turn on. """
        # Need to apply mqtt logic here to turn on led
        _LOGGER.debug(f"Turn on {self._name} (attr_name: {self._attr_name}) (unique: {self._attr_unique_id})")

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        # Need to apply mqtt logic here to turn off led
        _LOGGER.debug(f"Turn off {self._name} (attr_name: {self._attr_name}) (unique: {self._attr_unique_id})")

    def update(self) -> None:
        """Fetch new state data for this light."""
        # get latest stats from mqtt for this light
        # then update self._state
        _LOGGER.debug(f"Update {self._name} (attr_name: {self._attr_name}) (unique: {self._attr_unique_id})")

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {"identifiers": {(DOMAIN, self._hub_id)}}
