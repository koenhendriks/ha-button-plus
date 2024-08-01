"""Platform for button integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from functools import cached_property
from typing import Any

from homeassistant.components.button import ButtonEntity, ButtonDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import (
    AddEntitiesCallback,
    async_get_current_platform,
)

from .button_plus_api.model_interface import Connector, ConnectorType
from .const import DOMAIN
from . import ButtonPlusHub

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=30)
SERVICE_LONG_PRESS = "long_press"
SERVICE_RELEASE = "release"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add button_entities for passed config_entry in HA."""

    button_entities: list[ButtonPlusButton] = []
    hub: ButtonPlusHub = hass.data[DOMAIN][config_entry.entry_id]

    active_connectors = [
        connector.identifier()
        for connector in hub.config.connectors_for(ConnectorType.DISPLAY, ConnectorType.BAR)
    ]

    buttons = filter(
        lambda b: b.button_id // 2 in active_connectors, hub.config.buttons()
    )

    for button in buttons:
        _LOGGER.info(
            f"Creating button with parameters: {button.button_id} {button.top_label} {button.label} {hub.hub_id}"
        )
        entity = ButtonPlusButton(button.button_id, hub)
        button_entities.append(entity)
        hub.add_button(button.button_id, entity)

    async_add_entities(button_entities)

    platform = async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_LONG_PRESS,
        {},
        "_async_long_press_action",
    )

    platform.async_register_entity_service(
        SERVICE_RELEASE,
        {},
        "_async_release_action",
    )


class ButtonPlusButton(ButtonEntity):
    _attr_click_type: str | None = None

    def __init__(self, btn_id: int, hub: ButtonPlusHub):
        self._is_on = False
        self._hub_id = hub.hub_id
        self._hub = hub
        self._btn_id = btn_id
        self.entity_id = f"button.{self._hub_id}_{btn_id}"
        self._attr_name = f"button-{btn_id}"
        self._name = f"Button {btn_id}"
        self._device_class = ButtonDeviceClass.IDENTIFY
        self._connector: Connector = hub.config.connector_for(btn_id // 2)
        self.unique_id = self.unique_id_gen()

    def unique_id_gen(self):
        match self._connector.connector_type():
            case ConnectorType.BAR:
                return self.unique_id_gen_bar()
            case ConnectorType.DISPLAY:
                return self.unique_id_gen_display()

    def unique_id_gen_bar(self):
        return f"button_{self._hub_id}_{self._btn_id}_bar_module_{self._connector.identifier()}"

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

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.debug(f"async press from mqtt button: {self._btn_id}")

    async def _async_long_press_action(self) -> None:
        self._attr_click_type = "long"
        await super()._async_press_action()

    async def _async_press_action(self) -> None:
        self._attr_click_type = "single"
        await super()._async_press_action()

    async def _async_release_action(self) -> None:
        # Not implemented
        pass

    @property
    def state_attributes(self) -> dict[str, Any] | None:
        return {
            "click_type": self._attr_click_type,
        }

    @cached_property
    def click_type(self) -> str | None:
        return self._attr_click_type
