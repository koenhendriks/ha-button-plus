""" Platform for button integration. """
from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity, ButtonDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import ButtonPlusHub

from .const import DOMAIN, MANUFACTURER

_LOGGER = logging.getLogger(__name__)

button_entities = []


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Add button_entities for passed config_entry in HA."""

    hub: ButtonPlusHub = hass.data[DOMAIN][config_entry.entry_id]

    active_connectors = [connector.connector_id for connector in filter(lambda c: c.connector_type in [1,2],hub.config.info.connectors)]
    buttons = filter(lambda b: b.button_id//2 in active_connectors,hub.config.mqtt_buttons)

    for button in buttons:
        _LOGGER.debug(f"Creating button with parameters: {button.button_id} {button.label} {hub.hub_id}")
        entity = ButtonPlusButton(button.button_id, hub)
        button_entities.append(entity)
        hub.add_button(button.button_id, entity)

    async_add_entities(button_entities)


class ButtonPlusButton(ButtonEntity):
    def __init__(self, btn_id: int, hub: ButtonPlusHub):
        self._is_on = False
        self._hub_id = hub.hub_id
        self._hub = hub
        self._btn_id = btn_id
        self._attr_unique_id = f'button-{self._hub_id}-{btn_id}'
        self.entity_id = f"button.{self._hub_id}_{btn_id}"
        self._attr_name = f'button-{btn_id}'
        self._name = f'Button {btn_id}'
        self._device_class = ButtonDeviceClass.IDENTIFY
        self._connector = hub.config.info.connectors[btn_id//2]

    @property
    def name(self) -> str:
        """Return the display name of this button."""
        return self._name

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        device_info = {
            "via_device": (DOMAIN, self._hub.hub_id),
            "manufacturer": MANUFACTURER,
        }

        match self._connector.connector_type:
            case 1:
                device_info["name"] = f"BAR Module {self._connector.connector_id}"
                device_info["connections"] = {("bar_module", self._connector.connector_id)}
                device_info["model"] = "BAR Module"
                device_info["identifiers"] = {(DOMAIN, f'{self._btn_id}_bar_module_{self._connector.connector_id}')}
            case 2:
                device_info["name"] = f"Display Module"
                device_info["connections"] = {("display_module", 1)}
                device_info["model"] = "Display Module"
                device_info["identifiers"] = {(DOMAIN, f'{self._btn_id}_display_module')}

        return device_info

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.debug(f"async press from mqtt button: {self._btn_id}")
