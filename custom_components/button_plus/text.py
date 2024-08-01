"""Platform for text integration."""

from __future__ import annotations

import logging
from typing import Any, List

from homeassistant.components.text import TextEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.mqtt import client as mqtt
from homeassistant.helpers import template
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo

from . import ButtonPlusHub
from .button_plus_api.model_interface import ConnectorType
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add text entity for each top and main label from config_entry in HA."""

    text_entities: List[ButtonPlusText] = []
    hub: ButtonPlusHub = hass.data[DOMAIN][config_entry.entry_id]

    active_connectors = [
        connector.identifier()
        for connector in hub.config.connectors_for(
            ConnectorType.DISPLAY, ConnectorType.BAR
        )
    ]

    buttons = filter(
        lambda b: b.button_id // 2 in active_connectors, hub.config.buttons()
    )

    for button in buttons:
        _LOGGER.info(
            f"Creating texts with parameters: {button.button_id} {button.top_label} {button.label} {hub.hub_id}"
        )

        label_entity = ButtonPlusLabel(button.button_id, hub, button.label)
        text_entities.append(label_entity)
        hub.add_label(button.button_id, label_entity)

        top_label_entity = ButtonPlusTopLabel(button.button_id, hub, button.top_label)
        text_entities.append(top_label_entity)
        hub.add_top_label(button.button_id, top_label_entity)

    async_add_entities(text_entities)


class ButtonPlusText(TextEntity):
    def __init__(self, btn_id: int, hub: ButtonPlusHub, btn_label: str, text_type: str):
        self._hub_id = hub.hub_id
        self._hub = hub
        self._btn_id = btn_id
        self._text_type = text_type
        self.entity_id = f"text.{text_type}_{self._hub_id}_{btn_id}"
        self._attr_name = f"text-{text_type}-{btn_id}"
        self._attr_native_value = btn_label
        self._connector = hub.config.connector_for(btn_id // 2)
        self.unique_id = self.unique_id_gen()

    def unique_id_gen(self):
        match self._connector.connector_type():
            case ConnectorType.BAR:
                return self.unique_id_gen_bar()
            case ConnectorType.DISPLAY:
                return self.unique_id_gen_display()

    def unique_id_gen_bar(self):
        return f"text_{self._hub_id}_{self._btn_id}_bar_module_{self._connector.identifier()}_{self._text_type}"

    def unique_id_gen_display(self):
        return f"text_{self._hub_id}_{self._btn_id}_display_module_{self._text_type}"

    @property
    def should_poll(self) -> bool:
        return False

    def update(self) -> None:
        """Fetch new state data for this label."""
        # get latest stats from mqtt for this label
        # then update self._state
        _LOGGER.debug(
            f"Update {self.name} (attr_name: {self._attr_name}) (unique: {self._attr_unique_id})"
        )

    @property
    def device_info(self) -> DeviceInfo:
        """Return information to link this entity with the correct device."""

        identifiers: set[tuple[str, str]] = set()

        match self._connector.connector_type():
            case ConnectorType.BAR:
                identifiers = {
                    (
                        DOMAIN,
                        f"{self._hub.hub_id} BAR Module {self._connector.identifier()}",
                    )
                }
            case ConnectorType.DISPLAY:
                identifiers = {(DOMAIN, f"{self._hub.hub_id} Display Module")}

        return DeviceInfo(
            identifiers=identifiers,
        )

    async def async_set_value(self, value: str) -> None:
        """Set the text value and publish to mqtt."""
        parse_value: Any = template.Template(value, self.hass).async_render(
            parse_result=False
        )

        label_topic = (
            f"buttonplus/{self._hub_id}/button/{self._btn_id}/{self._text_type}"
        )
        _LOGGER.debug(f"ButtonPlus label update for {self.entity_id}")
        _LOGGER.debug(
            f"ButtonPlus label update to {label_topic} with new value: {parse_value}"
        )
        await mqtt.async_publish(
            hass=self.hass, topic=label_topic, payload=parse_value, qos=0, retain=True
        )
        self._attr_native_value = parse_value
        self.async_write_ha_state()


class ButtonPlusLabel(ButtonPlusText):
    """Wall label entity representation"""

    def __init__(self, btn_id: int, hub: ButtonPlusHub, label: str):
        super().__init__(btn_id, hub, label, "label")

    @property
    def name(self) -> str:
        """Return the display name of this label."""
        return f"Label {self._btn_id}"


class ButtonPlusTopLabel(ButtonPlusText):
    """Wall label entity representation"""

    def __init__(self, btn_id: int, hub: ButtonPlusHub, label: str):
        super().__init__(btn_id, hub, label, "top_label")

    @property
    def name(self) -> str:
        """Return the display name of this label."""
        return f"Top Label {self._btn_id}"
