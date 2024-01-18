from homeassistant.components.button import ButtonEntity
from . import DOMAIN, ButtonPlusHub
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.components.mqtt import client as mqtt, ReceiveMessage

import logging
import re

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
        self._mqtt_topic_buttons = f"buttonplus/{hub.hub_id}/button/+/click"

    async def _async_update_data(self):
        """Create MQTT subscriptions for buttonplus """
        _LOGGER.debug(f"Initial data fetch from coordinator")
        if not self._mqtt_subscribed_buttons:
            self.unsubscribe_mqtt = await mqtt.async_subscribe(
                self._hass,
                self._mqtt_topic_buttons,
                self.mqtt_button_callback,
                0
            )
            _LOGGER.debug(f"MQTT subscribed to {self._mqtt_topic_buttons}")

    async def mqtt_button_callback(self, message: ReceiveMessage):
        # Handle the message here
        _LOGGER.debug(f"Received message on topic {message.topic}: {message.payload}")
        match = re.search(r'/(\d+)/click', message.topic)
        btn_id = int(match.group(1)) if match else None

        entity: ButtonEntity = self.hub.button_entities[str(btn_id)]

        await self.hass.services.async_call(
            "button",
            'press',
            target={"entity_id": entity.entity_id}
        )

