""" Platform for text integration. """
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.text import TextEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import ButtonPlusHub

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

texts = []


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Add switches for passed config_entry in HA."""

    hub: ButtonPlusHub = hass.data[DOMAIN][config_entry.entry_id]
    buttons = hub.config.mqtt_buttons

    for button in buttons:
        _LOGGER.debug(f"Creating Texts with parameters: {button.button_id} {button.top_label} {button.label} {hub.hub_id}")
        texts.append(ButtonPlusLabel(button.button_id, hub.hub_id, button.label))
        texts.append(ButtonPlusTopLabel(button.button_id, hub.hub_id, button.top_label))

    async_add_entities(texts)


class ButtonPlusText(TextEntity):
    def __init__(self, btn_id: int, hub_id: str, btn_label: str, text_type: str):
        self._btn_id = btn_id
        self._hub_id = hub_id
        self._text_type = text_type
        self._attr_unique_id = f'text-{text_type}-{hub_id}-{btn_id}'
        self.entity_id = f"text.{text_type}_{hub_id}_{btn_id}"
        self._attr_name = f'text-{text_type}-{btn_id}'
        self._attr_native_value = btn_label

    def update(self) -> None:
        """Fetch new state data for this label."""
        # get latest stats from mqtt for this label
        # then update self._state
        _LOGGER.debug(f"Update {self.name} (attr_name: {self._attr_name}) (unique: {self._attr_unique_id})")

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {"identifiers": {(DOMAIN, self._hub_id)}}

    def set_value(self, value: str) -> None:
        """Set the text value."""
        self._attr_native_value = value

    async def async_set_value(self, value: str) -> None:
        """Set the text value from mqtt."""
        self._attr_native_value = value


class ButtonPlusLabel(ButtonPlusText):
    """ Wall label entity representation """

    def __init__(self, btn_id: int, hub_id: str, label: str):
        super().__init__(btn_id, hub_id, label, "label")

    @property
    def name(self) -> str:
        """Return the display name of this label."""
        return f'Label {self._btn_id}'


class ButtonPlusTopLabel(ButtonPlusText):
    """ Wall label entity representation """

    def __init__(self, btn_id: int, hub_id: str, label: str):
        super().__init__(btn_id, hub_id, label, "top_label")

    @property
    def name(self) -> str:
        """Return the display name of this label."""
        return f'Top Label {self._btn_id}'
