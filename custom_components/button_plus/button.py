"""Platform for button integration."""

from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity, ButtonDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo

from .button_plus_api.model import Connector, ConnectorEnum
from .const import DOMAIN
from . import ButtonPlusHub

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add button_entities for passed config_entry in HA."""

    button_entities: list[ButtonPlusButton] = []
    hub: ButtonPlusHub = hass.data[DOMAIN][config_entry.entry_id]

    active_connectors = active_connectors = [
        connector.connector_id
        for connector in hub.config.info.connectors
        if connector.connector_type_enum() in [ConnectorEnum.DISPLAY, ConnectorEnum.BAR]
    ]

    buttons = filter(
        lambda b: b.button_id // 2 in active_connectors, hub.config.mqtt_buttons
    )

    for button in buttons:
        _LOGGER.debug(
            f"Creating button with parameters: {button.button_id} {button.label} {hub.hub_id}"
        )
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
        self.entity_id = f"button.{self._hub_id}_{btn_id}"
        self._attr_name = f"button-{btn_id}"
        self._name = f"Button {btn_id}"
        self._device_class = ButtonDeviceClass.IDENTIFY
        self._connector: Connector = hub.config.info.connectors[btn_id // 2]
        self.unique_id = self.unique_id_gen()

    def unique_id_gen(self):
        match self._connector.connector_type_enum():
            case ConnectorEnum.BAR:
                return self.unique_id_gen_bar()
            case ConnectorEnum.DISPLAY:
                return self.unique_id_gen_display()

    def unique_id_gen_bar(self):
        return f"button_{self._hub_id}_{self._btn_id}_bar_module_{self._connector.connector_id}"

    def unique_id_gen_display(self):
        return f"button_{self._hub_id}_{self._btn_id}_display_module"

    @property
    def name(self) -> str:
        """Return the display name of this button."""
        return self._name

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def device_info(self) -> DeviceInfo:
        """Return information to link this entity with the correct device."""

        identifiers: set[tuple[str, str]] = {}

        match self._connector.connector_type_enum():
            case ConnectorEnum.BAR:
                identifiers = {
                    (
                        DOMAIN,
                        f"{self._hub.hub_id} BAR Module {self._connector.connector_id}",
                    )
                }
            case ConnectorEnum.DISPLAY:
                identifiers = {(DOMAIN, f"{self._hub.hub_id} Display Module")}

        return DeviceInfo(
            identifiers=identifiers,
        )

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.debug(f"async press from mqtt button: {self._btn_id}")
