from typing import List, Dict, Any
from .model_v1_07 import (
    Connector,
    Sensor,
    Topic,
    MqttButton,
    MqttBroker,
    MqttSensor,
    DeviceConfiguration as DeviceConfiguration_v1_07,
)


class Info:
    def __init__(
        self,
        device_id: str,
        mac: str,
        ip_address: str,
        firmware: str,
        large_display: int,
        connectors: List[Connector],
        sensors: List[Sensor],
    ):
        self.device_id = device_id
        self.mac = mac
        self.ip_address = ip_address
        self.firmware = firmware
        self.large_display = large_display
        self.connectors = connectors
        self.sensors = sensors

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Info":
        return Info(
            device_id=data["id"],
            mac=data["mac"],
            ip_address=data["ipaddress"],
            firmware=data["firmware"],
            large_display=data["largedisplay"],
            connectors=[
                Connector.from_dict(connector) for connector in data["connectors"]
            ],
            sensors=[Sensor.from_dict(sensor) for sensor in data["sensors"]],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.device_id,
            "mac": self.mac,
            "ipaddress": self.ip_address,
            "firmware": self.firmware,
            "largedisplay": self.large_display,
            "connectors": [connector.to_dict() for connector in self.connectors],
            "sensors": [sensor.to_dict() for sensor in self.sensors],
        }


class Core:
    def __init__(
        self,
        name: str,
        location: str,
        auto_backup: bool,
        brightness: int,
        color: int,
        statusbar: int,
        topics: List[Topic],
    ):
        self.name = name
        self.location = location
        self.auto_backup = auto_backup
        self.brightness = brightness
        self.color = color
        self.statusbar = statusbar
        self.topics = topics

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Core":
        return Core(
            name=data["name"],
            location=data["location"],
            auto_backup=data["autobackup"],
            brightness=data["brightness"],
            color=data["color"],
            statusbar=data["statusbar"],
            topics=[Topic.from_dict(topic) for topic in data["topics"]],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "location": self.location,
            "autobackup": self.auto_backup,
            "brightness": self.brightness,
            "color": self.color,
            "statusbar": self.statusbar,
            "topics": [topic.to_dict() for topic in self.topics],
        }


class MqttDisplay:
    def __init__(
        self,
        align: int,
        x: int,
        y: int,
        box_type: int,
        font_size: int,
        page: int,
        label: str,
        width: int,
        unit: str,
        round: int,
        topics: List[Topic],
    ):
        self.x = x
        self.y = y
        self.box_type = box_type
        self.font_size = font_size
        self.align = align
        self.width = width
        self.label = label
        self.unit = unit
        self.round = round
        self.page = page
        self.topics = topics

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MqttDisplay":
        return MqttDisplay(
            x=data["x"],
            y=data["y"],
            box_type=data["boxtype"],
            font_size=data["fontsize"],
            align=data["align"],
            width=data["width"],
            label=data["label"],
            unit=data["unit"],
            round=data["round"],
            page=data["page"],
            topics=[Topic.from_dict(topic) for topic in data["topics"]],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "boxtype": self.box_type,
            "fontsize": self.font_size,
            "align": self.align,
            "width": self.width,
            "label": self.label,
            "unit": self.unit,
            "round": self.round,
            "page": self.page,
            "topics": [topic.to_dict() for topic in self.topics],
        }


class DeviceConfiguration(DeviceConfiguration_v1_07):
    # Info, Core and MqttDisplay are different, so we need to redefine those
    def __init__(
        self,
        info: Info,
        core: Core,
        mqtt_buttons: List[MqttButton],
        mqtt_displays: List[MqttDisplay],
        mqtt_brokers: List[MqttBroker],
        mqtt_sensors: List[MqttSensor],
    ):
        self.info = info
        self.core = core
        self.mqtt_buttons = mqtt_buttons
        self.mqtt_displays = mqtt_displays
        self.mqtt_brokers = mqtt_brokers
        self.mqtt_sensors = mqtt_sensors

    # Same here, use the new classes for Info, Core and MqttDisplay
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "DeviceConfiguration":
        return DeviceConfiguration(
            info=Info.from_dict(data["info"]),
            core=Core.from_dict(data["core"]),
            mqtt_buttons=[
                MqttButton.from_dict(button) for button in data["mqttbuttons"]
            ],
            mqtt_displays=[
                MqttDisplay.from_dict(display) for display in data["mqttdisplays"]
            ],
            mqtt_brokers=[
                MqttBroker.from_dict(broker) for broker in data["mqttbrokers"]
            ],
            mqtt_sensors=[
                MqttSensor.from_dict(sensor) for sensor in data["mqttsensors"]
            ],
        )
