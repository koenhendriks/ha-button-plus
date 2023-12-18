""" Platform for switch integration. """
from __future__ import annotations

import json
import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.switch import (SwitchEntity, PLATFORM_SCHEMA, SwitchDeviceClass)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import UndefinedType

from .const import DOMAIN

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
})

_LOGGER = logging.getLogger(__name__)

switches = []


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Add switches for passed config_entry in HA."""
    # The hub is loaded from the associated hass.data entry that was created in the
    # __init__.async_setup_entry function
    _LOGGER.debug(f"{DOMAIN} - hass config loaded - config: {config_entry}")

    hub = hass.data[DOMAIN][config_entry.entry_id]

    for base in hub.devices:
        _LOGGER.debug(f"base id: {base.button_plus_base_id}")

        bp_config = await base.hub.client.fetch_config(base.button_plus_base_id)

        data = json.loads(bp_config)
        buttons = data['mqttbuttons']
        # _LOGGER.debug(f"{DOMAIN} - fetched buttons: {buttons}")

        for button in buttons:
            switches.append(ButtonPlusSwitch(button['id'], button.get('label', 'No label'), base.button_plus_base_id))

    async_add_entities(switches)


class ButtonPlusSwitch(SwitchEntity):
    """ Representation of a button+ switch """
    _attr_has_entity_name = True

    def __init__(self, btn_id, btn_label, hub_id):
        self._is_on = False
        self._attr_unique_id = f'bp-{hub_id}-{btn_id}'
        self._attr_name = btn_label
        self._hub_id = hub_id
        self._device_class = SwitchDeviceClass.SWITCH

    @property
    def name(self) -> str | UndefinedType | None:
        return self._attr_name

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {"identifiers": {(DOMAIN, self._hub_id)}}

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._is_on

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._is_on = True

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._is_on = False
