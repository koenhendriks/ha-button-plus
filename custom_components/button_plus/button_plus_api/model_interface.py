from typing import List

from button_plus.button_plus_api.connector_type import ConnectorType


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


class DeviceConfiguration:
    @staticmethod
    def from_json(json_data: str) -> "DeviceConfiguration":
        """Deserialize the DeviceConfiguration from a JSON string."""
        pass

    def to_json(self) -> str:
        """Serialize the DeviceConfiguration to a JSON string."""
        pass

    def firmware_version(self) -> str:
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
