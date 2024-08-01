import json
import logging
from typing import List, Dict, Any

from packaging.version import parse as parseVersion, Version

from .JSONCustomEncoder import CustomEncoder
from .connector_type import ConnectorType
from .event_type import EventType
from .model_interface import Button

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Connector:
    def __init__(self, identifier: int, connector_type: ConnectorType):
        self._identifier = identifier
        self._connector_type = connector_type

    def identifier(self) -> int:
        return self._identifier

    def connector_type(self) -> ConnectorType:
        return ConnectorType(self._connector_type)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Connector":
        return Connector(
            identifier=data["id"], connector_type=ConnectorType(data["type"])
        )

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self._identifier, "type": self._connector_type}


class Sensor:
    def __init__(self, sensor_id: int, description: str):
        self.sensor_id = sensor_id
        self.description = description

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Sensor":
        return Sensor(sensor_id=data["sensorid"], description=data["description"])

    def to_dict(self) -> Dict[str, Any]:
        return {"sensorid": self.sensor_id, "description": self.description}


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
        self.connectors: List[Connector] = connectors
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


class Topic:
    def __init__(self, broker_id: str, topic: str, payload: str, event_type: EventType):
        self.broker_id = broker_id
        self.topic = topic
        self.payload = payload
        self.event_type = event_type

    def connector_type_enum(self) -> EventType:
        return EventType(self.event_type)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Topic":
        return Topic(
            broker_id=data["brokerid"],
            topic=data["topic"],
            payload=data["payload"],
            event_type=EventType(data["eventtype"]),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "brokerid": self.broker_id,
            "topic": self.topic,
            "payload": self.payload,
            "eventtype": self.event_type,
        }


class Core:
    def __init__(
        self,
        name: str,
        location: str,
        auto_backup: bool,
        brightness_large_display: int,
        brightness_mini_display: int,
        led_color_front: int,
        led_color_wall: int,
        color: int,
        topics: List[Topic],
    ):
        self.name = name
        self.location = location
        self.auto_backup = auto_backup
        self.brightness_large_display = brightness_large_display
        self.brightness_mini_display = brightness_mini_display
        self.led_color_front = led_color_front
        self.led_color_wall = led_color_wall
        self.color = color
        self.topics = topics

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Core":
        return Core(
            name=data["name"],
            location=data["location"],
            auto_backup=data["autobackup"],
            brightness_large_display=data["brightnesslargedisplay"],
            brightness_mini_display=data["brightnessminidisplay"],
            led_color_front=data["ledcolorfront"],
            led_color_wall=data["ledcolorwall"],
            color=data["color"],
            topics=[Topic.from_dict(topic) for topic in data.get("topics", [])],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "location": self.location,
            "autobackup": self.auto_backup,
            "brightnesslargedisplay": self.brightness_large_display,
            "brightnessminidisplay": self.brightness_mini_display,
            "ledcolorfront": self.led_color_front,
            "ledcolorwall": self.led_color_wall,
            "color": self.color,
            # Only the Core object does not include the key when this list is empty (-:
            **(
                {"topics": [topic.to_dict() for topic in self.topics]}
                if len(self.topics) > 0
                else {}
            ),
        }


class MqttButton(Button):
    def __init__(
        self,
        button_id: int,
        label: str,
        top_label: str,
        led_color_front: int,
        led_color_wall: int,
        long_delay: int,
        long_repeat: int,
        topics: List[Topic],
    ):
        self.button_id = button_id
        self.label = label
        self.top_label = top_label
        self.led_color_front = led_color_front
        self.led_color_wall = led_color_wall
        self.long_delay = long_delay
        self.long_repeat = long_repeat
        self.topics = topics

    def add_topic(self, topic: str, event_type: EventType, payload: str = "") -> None:
        self.topics.append(Topic("ha-button-plus", topic, payload, event_type))

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MqttButton":
        return MqttButton(
            button_id=data["id"],
            label=data["label"],
            top_label=data["toplabel"],
            led_color_front=data["ledcolorfront"],
            led_color_wall=data["ledcolorwall"],
            long_delay=data["longdelay"],
            long_repeat=data["longrepeat"],
            topics=[Topic.from_dict(topic) for topic in data.get("topics", [])],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.button_id,
            "label": self.label,
            "toplabel": self.top_label,
            "ledcolorfront": self.led_color_front,
            "ledcolorwall": self.led_color_wall,
            "longdelay": self.long_delay,
            "longrepeat": self.long_repeat,
            "topics": [topic.to_dict() for topic in self.topics],
        }


class MqttDisplay:
    def __init__(
        self,
        x: int,
        y: int,
        font_size: int,
        align: int,
        width: int,
        label: str,
        unit: str,
        round: int,
        topics: List[Topic],
    ):
        self.x = x
        self.y = y
        self.font_size = font_size
        self.align = align
        self.width = width
        self.label = label
        self.unit = unit
        self.round = round
        self.topics = topics

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MqttDisplay":
        return MqttDisplay(
            x=data["x"],
            y=data["y"],
            font_size=data["fontsize"],
            align=data["align"],
            width=data["width"],
            label=data["label"],
            unit=data["unit"],
            round=data["round"],
            topics=[Topic.from_dict(topic) for topic in data.get("topics", [])],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "fontsize": self.font_size,
            "align": self.align,
            "width": self.width,
            "label": self.label,
            "unit": self.unit,
            "round": self.round,
            "topics": [topic.to_dict() for topic in self.topics],
        }


class MqttBroker:
    def __init__(
        self,
        url: str,
        port: int,
        username: str,
        password: str,
        broker_id="ha-button-plus",
        ws_port=9001,
    ):
        self.url = url
        self.port = port
        self.username = username
        self.password = password
        self.broker_id = broker_id
        self.ws_port = ws_port

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MqttBroker":
        return MqttBroker(
            broker_id=data["brokerid"] or "ha-button-plus",
            url=data["url"],
            port=data["port"],
            ws_port=data["wsport"],
            username=data["username"],
            password=data["password"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "brokerid": self.broker_id or "ha-button-plus",
            "url": self.url,
            "port": self.port,
            "wsport": self.ws_port,
            "username": self.username,
            "password": self.password,
        }


class MqttSensor:
    def __init__(self, sensor_id: int, topic: Topic, interval: int):
        self.sensor_id = sensor_id
        self.topic = topic
        self.interval = interval

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MqttSensor":
        return MqttSensor(
            sensor_id=data["sensorid"],
            topic=Topic.from_dict(data["topic"]),
            interval=data["interval"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sensorid": self.sensor_id,
            "topic": self.topic.to_dict(),
            "interval": self.interval,
        }


class DeviceConfiguration:
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

    def firmware_version(self) -> Version:
        return parseVersion(self.info.firmware)

    def supports_brightness(self) -> bool:
        return self.firmware_version() >= parseVersion("1.11")

    def name(self) -> str:
        return self.core.name or self.info.device_id

    def identifier(self) -> str:
        return self.info.device_id

    def ip_address(self) -> str:
        return self.info.ip_address

    def mac_address(self) -> str:
        return self.info.mac

    def location(self) -> str:
        return self.core.location

    def connector_for(self, identifier: int) -> Connector:
        return next(
            (
                connector
                for connector in self.info.connectors
                if connector.identifier() == identifier
            ),
            None,
        )

    def connectors_for(self, *connector_type: ConnectorType) -> List[Connector]:
        _LOGGER.debug(
            f"Filter all {len(self.info.connectors)} connectors by type {connector_type}"
        )
        return [
            connector
            for connector in self.info.connectors
            if connector.connector_type() in connector_type
        ]

    def connectors(self) -> List[Connector]:
        return self.info.connectors

    def buttons(self) -> List[Button]:
        return [button for button in self.mqtt_buttons]

    def set_broker(self, url: str, port: int, username: str, password: str) -> None:
        self.mqtt_brokers.append(MqttBroker(url, port, username, password))

    def add_topic(self, topic: str, event_type: EventType) -> None:
        self.core.topics.append(
            Topic(
                broker_id="ha-button-plus",
                topic=topic,
                payload="",
                event_type=event_type,
            )
        )

    def remove_topic_for(self, event_type: EventType) -> None:
        # Remove the topic with EventType event_type
        self.core.topics = [
            topic for topic in self.core.topics if topic.event_type != event_type
        ]

    def topics(self) -> List[Topic]:
        return self.core.topics

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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "info": self.info.to_dict(),
            "core": self.core.to_dict(),
            "mqttbuttons": [button.to_dict() for button in self.mqtt_buttons],
            "mqttdisplays": [display.to_dict() for display in self.mqtt_displays],
            "mqttbrokers": [broker.to_dict() for broker in self.mqtt_brokers],
            "mqttsensors": [sensor.to_dict() for sensor in self.mqtt_sensors],
        }

    def to_json(self) -> str:
        return json.dumps(
            self,
            sort_keys=True,
            cls=CustomEncoder,
            indent=4,
        )
