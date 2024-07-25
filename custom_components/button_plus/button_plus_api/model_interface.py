from typing import List

from packaging.version import Version

from button_plus.button_plus_api.event_type import EventType
from custom_components.button_plus.button_plus_api.connector_type import ConnectorType


class Connector:
    def identifier(self) -> int:
        """Return the identifier of the connector."""
        pass

    def connector_type(self) -> ConnectorType:
        """Return the connector type."""
        pass


class Button:
    def button_id(self) -> int:
        """Return the identifier of the connector."""
        pass


class MqttBroker:
    url: str
    port: int
    username: str
    password: str

    def __init__(
            self,
            url: str,
            port: int,
            username: str,
            password: str,
    ):
        """Initialize the MQTT broker."""
        pass


class Topic:
    topic: str
    event_type: EventType

    def __init__(
            self,
            topic: str,
            event_type: EventType,
    ):
        """Initialize the MQTT topic."""
        pass


class DeviceConfiguration:
    @staticmethod
    def from_json(json_data: str) -> "DeviceConfiguration":
        """Deserialize the DeviceConfiguration from a JSON string."""
        pass

    def to_json(self) -> str:
        """Serialize the DeviceConfiguration to a JSON string."""
        pass

    def firmware_version(self) -> Version:
        """Return the firmware version of the device."""
        pass

    def name(self) -> str:
        """Return the name of the device."""
        pass

    def identifier(self) -> str:
        """Return the identifier of the device."""
        pass

    def ip_address(self) -> str:
        """Return the IP address of the device."""
        pass

    def mac_address(self) -> str:
        """Return the MAC address of the device."""
        pass

    def location(self) -> str:
        """Return the location description of the device."""
        pass

    def connectors_for(self, *connector_type: ConnectorType) -> List[Connector]:
        """Return the connectors of the given type."""
        pass

    def connector_for(self, *identifier: int) -> Connector:
        """Return the connectors of the given type."""
        pass

    def buttons(self) -> List[Button]:
        """Return the available buttons."""
        pass

    def get_broker(self) -> MqttBroker:
        """Return the MQTT broker."""
        pass

    def set_broker(self, broker: MqttBroker) -> None:
        """Set the MQTT broker."""
        pass

    def add_topic(self, topic: Topic) -> None:
        """Set the MQTT topic."""
        pass

    def remove_topic_for(self, event_type: EventType) -> None:
        """Remove the MQTT topic."""
        pass
