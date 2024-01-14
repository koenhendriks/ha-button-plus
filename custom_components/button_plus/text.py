""" Platform for text integration. """
from __future__ import annotations

import logging

from homeassistant.components.text import TextEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.mqtt import client as mqtt
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import ButtonPlusHub

from .const import DOMAIN, MANUFACTURER

_LOGGER = logging.getLogger(__name__)

text_entities = []


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    """Add text entity for each top and main label from config_entry in HA."""

    hub: ButtonPlusHub = hass.data[DOMAIN][config_entry.entry_id]

    active_connectors = [
        connector.connector_id
        for connector in hub.config.info.connectors
        if connector.connector_type in [1, 2]
    ]

    buttons = filter(lambda b: b.button_id // 2 in active_connectors, hub.config.mqtt_buttons)

    for button in buttons:
        _LOGGER.debug(
            f"Creating Texts with parameters: {button.button_id} {button.top_label} {button.label} {hub.hub_id}")

        label_entity = ButtonPlusLabel(button.button_id, hub, button.label)
        top_label_entity = ButtonPlusTopLabel(button.button_id, hub, button.top_label)

        text_entities.append(label_entity)
        text_entities.append(top_label_entity)

        hub.add_label(button.button_id, label_entity)
        hub.add_top_label(button.button_id, top_label_entity)

    async_add_entities(text_entities)


class ButtonPlusText(TextEntity):
    def __init__(self, btn_id: int, hub: ButtonPlusHub, btn_label: str, text_type: str):
        self._btn_id = btn_id
        self._hub = hub
        self._hub_id = hub.hub_id
        self._text_type = text_type
        self._attr_unique_id = f'text-{text_type}-{self._hub_id}-{btn_id}'
        self.entity_id = f"text.{text_type}_{self._hub_id}_{btn_id}"
        self._attr_name = f'text-{text_type}-{btn_id}'
        self._attr_native_value = btn_label
        self._connector = hub.config.info.connectors[btn_id // 2]

    @property
    def should_poll(self) -> bool:
        return False

    def update(self) -> None:
        """Fetch new state data for this label."""
        # get latest stats from mqtt for this label
        # then update self._state
        _LOGGER.debug(f"Update {self.name} (attr_name: {self._attr_name}) (unique: {self._attr_unique_id})")

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

    async def async_set_value(self, value: str) -> None:
        """Set the text value and publish to mqtt."""
        label_topic = f"buttonplus/{self._hub_id}/button/{self._btn_id}/{self._text_type}"
        _LOGGER.debug(f"ButtonPlus label update for {self.entity_id}")
        _LOGGER.debug(f"ButtonPlus label update to {label_topic} with new value: {value}")
        await mqtt.async_publish(hass=self.hass, topic=label_topic, payload=value, qos=0, retain=True)
        self._attr_native_value = value


class ButtonPlusLabel(ButtonPlusText):
    """ Wall label entity representation """

    def __init__(self, btn_id: int, hub: ButtonPlusHub, label: str):
        super().__init__(btn_id, hub, label, "label")

    @property
    def name(self) -> str:
        """Return the display name of this label."""
        return f'Label {self._btn_id}'


class ButtonPlusTopLabel(ButtonPlusText):
    """ Wall label entity representation """

    def __init__(self, btn_id: int, hub: ButtonPlusHub, label: str):
        super().__init__(btn_id, hub, label, "top_label")

    @property
    def name(self) -> str:
        """Return the display name of this label."""
        return f'Top Label {self._btn_id}'
