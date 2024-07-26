"""Platform for light integration."""

from __future__ import annotations

import logging

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.mqtt import client as mqtt
from .button_plus_api.event_type import EventType
from . import ButtonPlusHub

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add switches for passed config_entry in HA."""

    brightness = []

    hub: ButtonPlusHub = hass.data[DOMAIN][config_entry.entry_id]

    if hub.config.supports_brightness() is False:
        _LOGGER.info(
            "Current firmware version doesn't support brightness settings, it must be at least firmware version 1.11"
        )
        return

    _LOGGER.debug(f"Creating number with parameters: {hub.hub_id}")
    mini = ButtonPlusMiniBrightness(hub)
    brightness.append(mini)
    hub.add_brightness("mini", mini)

    large = ButtonPlusLargeBrightness(hub)
    brightness.append(large)
    hub.add_brightness("large", large)

    async_add_entities(brightness)


class ButtonPlusBrightness(NumberEntity):
    def __init__(self, hub: ButtonPlusHub, brightness_type: str, event_type: EventType):
        self._hub = hub
        self._hub_id = hub.hub_id
        self._brightness_type = brightness_type
        self.entity_id = f"brightness.{brightness_type}_{self._hub_id}"
        self._attr_name = f"brightness-{brightness_type}"
        self.event_type = event_type
        self._topics = hub.config.topics()
        self._attr_icon = "mdi:television-ambient-light"
        self._attr_unique_id = f"brightness_{brightness_type}-{self._hub_id}"

    @property
    def native_max_value(self) -> float:
        return 100

    @property
    def native_min_value(self) -> float:
        return 0

    @property
    def native_unit_of_measurement(self) -> str:
        return "%"

    def update(self) -> None:
        """Fetch new state data for this light."""
        # get latest stats from mqtt for this light
        # then update self._state
        _LOGGER.debug(
            f"Update {self.name} (attr_name: {self._attr_name}) (unique: {self._attr_unique_id})"
        )

    @property
    def device_info(self) -> DeviceInfo:
        """Return information to link this entity with the correct device."""

        identifiers: set[tuple[str, str]] = set()

        match self.event_type:
            case EventType.BRIGHTNESS_MINI_DISPLAY:
                # selects the first module it finds.
                identifiers = {
                    (DOMAIN, f"{self._hub.hub_id} BAR Module 1"),
                    (DOMAIN, f"{self._hub.hub_id} BAR Module 2"),
                    (DOMAIN, f"{self._hub.hub_id} BAR Module 3"),
                }
            case EventType.BRIGHTNESS_LARGE_DISPLAY:
                identifiers = {(DOMAIN, f"{self._hub.hub_id} Display Module")}

        return DeviceInfo(
            identifiers=identifiers,
        )

    async def async_set_native_value(self, value: float) -> None:
        """Set the text value and publish to mqtt."""
        label_topic = f"buttonplus/{self._hub_id}/brightness/{self._brightness_type}"
        _LOGGER.debug(f"ButtonPlus brightness update for {self.entity_id}")
        _LOGGER.debug(
            f"ButtonPlus brightness update to {label_topic} with new value: {value}"
        )
        await mqtt.async_publish(
            hass=self.hass, topic=label_topic, payload=value, qos=0, retain=True
        )
        self._attr_native_value = value
        self.async_write_ha_state()


class ButtonPlusMiniBrightness(ButtonPlusBrightness):
    """Numeric entity representation"""

    def __init__(self, hub: ButtonPlusHub):
        super().__init__(hub, "mini", EventType.BRIGHTNESS_MINI_DISPLAY)

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return "Brightness mini display"


class ButtonPlusLargeBrightness(ButtonPlusBrightness):
    """Numeric entity representation"""

    def __init__(self, hub: ButtonPlusHub):
        super().__init__(hub, "large", EventType.BRIGHTNESS_LARGE_DISPLAY)

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return "Brightness large display"
