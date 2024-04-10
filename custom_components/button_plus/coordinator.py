import logging
import re

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.components.number import NumberEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.components.mqtt import client as mqtt, ReceiveMessage

from .buttonplushub import ButtonPlusHub
from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


class ButtonPlusCoordinator(DataUpdateCoordinator):
    """Button Plus coordinator."""

    def __init__(self, hass: HomeAssistant, hub: ButtonPlusHub):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_coordinator",
            update_interval=None,
            update_method=None,
        )
        self.hub = hub
        self._hass = hass
        self._mqtt_subscribed_buttons = False
        self._mqtt_topics = [
            (f"buttonplus/{hub.hub_id}/button/+/click", self.mqtt_button_callback),
            (f"buttonplus/{hub.hub_id}/button/+/long_press", self.mqtt_button_long_press_callback),
            (f"buttonplus/{hub.hub_id}/brightness/+", self.mqtt_brightness_callback),
            (f"buttonplus/{hub.hub_id}/page/+", self.mqtt_page_callback),
        ]

    async def _async_update_data(self):
        """Create MQTT subscriptions for buttonplus"""
        _LOGGER.debug("Initial data fetch from coordinator")
        if not self._mqtt_subscribed_buttons:
            for topic, cb in self._mqtt_topics:
                self.unsubscribe_mqtt = await mqtt.async_subscribe(
                    self._hass,
                    topic,
                    cb,
                    0
                )
                _LOGGER.debug(f"MQTT subscribed to {topic}")

    @callback
    async def mqtt_page_callback(self, message: ReceiveMessage):
        # Handle the message here
        _LOGGER.debug(f"Received message on topic {message.topic}: {message.payload}")
        # match = re.search(r"/page/(\w+)", message.topic)
        # is 'status' or 'set'
        # page_type = match.group(1)

        # TODO: implement page control

    @callback
    async def mqtt_brightness_callback(self, message: ReceiveMessage):
        # Handle the message here
        _LOGGER.debug(f"Received message on topic {message.topic}: {message.payload}")
        match = re.search(r"/brightness/(\w+)", message.topic)
        brightness_type = match.group(1)

        entity: NumberEntity = self.hub.brightness_entities[brightness_type]

        value = float(message.payload)
        entity._attr_native_value = value
        entity.schedule_update_ha_state()

    @callback
    async def mqtt_button_callback(self, message: ReceiveMessage):
        # Handle the message here
        _LOGGER.debug(f"Received message on topic {message.topic}: {message.payload}")
        match = re.search(r"/(\d+)/click", message.topic)
        btn_id = int(match.group(1)) if match else None

        entity: ButtonEntity = self.hub.button_entities[str(btn_id)]

        await self.hass.services.async_call(
            "button", "press", target={"entity_id": entity.entity_id}
        )

    @callback
    async def mqtt_button_long_press_callback(self, message: ReceiveMessage):
        # Handle the message here
        _LOGGER.debug(f"Received message on topic {message.topic}: {message.payload}")
        match = re.search(r'/(\d+)/long_press', message.topic)
        btn_id = int(match.group(1)) if match else None

        entity: ButtonEntity = self.hub.button_entities[str(btn_id)]

        await self.hass.services.async_call(
            DOMAIN,
            'long_press',
            target={"entity_id": entity.entity_id}
        )
