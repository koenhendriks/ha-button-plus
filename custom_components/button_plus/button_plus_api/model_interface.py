from typing import List, Dict, Any

from packaging.version import Version

from custom_components.button_plus.button_plus_api.event_type import EventType
from custom_components.button_plus.button_plus_api.connector_type import ConnectorType


class Connector:
    def identifier(self) -> int:
        """Return the identifier of the connector."""
        pass

    def connector_type(self) -> ConnectorType:
        """Return the connector type."""
        pass


class Button:
    button_id: int
    top_label: str
    label: str

    def add_topic(self, topic: str, event_type: EventType, payload: str = "") -> None:
        """Set the MQTT topic."""
        pass


class Topic:
    topic: str
    event_type: EventType


class DeviceConfiguration:
    def firmware_version(self) -> Version:
        """Return the firmware version of the device."""
        pass

    def supports_brightness(self) -> bool:
        """Return if the device supports brightness."""
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

    def connector_for(self, identifier: int) -> Connector:
        """Return the connectors of the given type."""
        pass

    def connectors(self) -> List[Connector]:
        """Return the connectors of the given type."""
        pass

    def buttons(self) -> List[Button]:
        """Return the available buttons."""
        pass

    def set_broker(self, url: str, port: int, username: str, password: str) -> None:
        """Set the MQTT broker."""
        pass

    def add_topic(self, topic: str, event_type: EventType) -> None:
        """Set the MQTT topic."""
        pass

    def remove_topic_for(self, event_type: EventType) -> None:
        """Remove the MQTT topic."""
        pass

    def topics(self) -> List[Topic]:
        """
        :return: List of topics for the device
        """
        pass

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "DeviceConfiguration":
        """Deserialize the DeviceConfiguration from a dictionary."""
        pass

    def to_json(self) -> str:
        """Serialize the DeviceConfiguration to a JSON string."""
        pass
