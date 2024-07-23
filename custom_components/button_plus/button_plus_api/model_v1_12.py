import json
from typing import List, Dict, Any

from .connector_type import ConnectorEnum
from .event_type import EventType


import json
from typing import List, Dict, Any

class Connector:
    def __init__(self, connector_id: int, connector_type: int):
        self.connector_id = connector_id
        self.connector_type = connector_type

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Connector":
        return Connector(connector_id=data["id"], connector_type=data["type"])

class Sensor:
    def __init__(self, sensor_id: int, description: str):
        self.sensor_id = sensor_id
        self.description = description

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Sensor":
        return Sensor(sensor_id=data["sensorid"], description=data["description"])

class Info:
    def __init__(self, device_id: str, mac: str, ip_address: str, firmware: str, large_display: int, connectors: List[Connector], sensors: List[Sensor]):
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
            connectors=[Connector.from_dict(connector) for connector in data["connectors"]],
            sensors=[Sensor.from_dict(sensor) for sensor in data["sensors"]]
        )

class Topic:
    def __init__(self, broker_id: str, topic: str, payload: str, event_type: int):
        self.broker_id = broker_id
        self.topic = topic
        self.payload = payload
        self.event_type = event_type

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Topic":
        return Topic(
            broker_id=data["brokerid"],
            topic=data["topic"],
            payload=data["payload"],
            event_type=data["eventtype"]
        )

class Core:
    def __init__(self, name: str, location: str, auto_backup: bool, brightness: int, color: int, statusbar: int, topics: List[Topic]):
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
            topics=[Topic.from_dict(topic) for topic in data["topics"]]
        )

class MqttButton:
    def __init__(self, button_id: int, label: str, top_label: str, led_color_front: int, led_color_wall: int, long_delay: int, long_repeat: int, topics: List[Topic]):
        self.button_id = button_id
        self.label = label
        self.top_label = top_label
        self.led_color_front = led_color_front
        self.led_color_wall = led_color_wall
        self.long_delay = long_delay
        self.long_repeat = long_repeat
        self.topics = topics

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
            topics=[Topic.from_dict(topic) for topic in data["topics"]]
        )

class MqttDisplay:
    def __init__(self, align: int, x: int, y: int, box_type: int, font_size: int, page: int, label: str, width: int, unit: str, round: int, topics: List[Topic]):
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
            topics=[Topic.from_dict(topic) for topic in data["topics"]]
        )

class MqttBroker:
    def __init__(self, broker_id: str, url: str, port: int, ws_port: int, username: str, password: str):
        self.broker_id = broker_id
        self.url = url
        self.port = port
        self.ws_port = ws_port
        self.username = username
        self.password = password

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MqttBroker":
        return MqttBroker(
            broker_id=data["brokerid"],
            url=data["url"],
            port=data["port"],
            ws_port=data["wsport"],
            username=data["username"],
            password=data["password"]
        )

class MqttSensor:
    def __init__(self, sensor_id: int, interval: int, topic: Topic):
        self.sensor_id = sensor_id
        self.interval = interval
        self.topic = topic

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MqttSensor":
        return MqttSensor(
            sensor_id=data["sensorid"],
            interval=data["interval"],
            topic=Topic.from_dict(data["topic"])
        )

class DeviceConfiguration:
    def __init__(self, info: Info, core: Core, mqtt_buttons: List[MqttButton], mqtt_displays: List[MqttDisplay], mqtt_brokers: List[MqttBroker], mqtt_sensors: List[MqttSensor]):
        self.info = info
        self.core = core
        self.mqtt_buttons = mqtt_buttons
        self.mqtt_displays = mqtt_displays
        self.mqtt_brokers = mqtt_brokers
        self.mqtt_sensors = mqtt_sensors

    @staticmethod
    def from_json(json_data: any) -> "DeviceConfiguration":
        return DeviceConfiguration(
            info=Info.from_dict(json_data["info"]),
            core=Core.from_dict(json_data["core"]),
            mqtt_buttons=[MqttButton.from_dict(button) for button in json_data["mqttbuttons"]],
            mqtt_displays=[MqttDisplay.from_dict(display) for display in json_data["mqttdisplays"]],
            mqtt_brokers=[MqttBroker.from_dict(broker) for broker in json_data["mqttbrokers"]],
            mqtt_sensors=[MqttSensor.from_dict(sensor) for sensor in json_data["mqttsensors"]]
        )

    def to_json(self) -> str:
        def serialize(obj):
            if hasattr(obj, "__dict__"):
                d = obj.__dict__.copy()

                if isinstance(obj, DeviceConfiguration):
                    d["info"] = serialize(d.pop("info"))
                    d["core"] = serialize(d.pop("core"))
                    d["mqttbuttons"] = [serialize(button) for button in d.pop("mqtt_buttons")]
                    d["mqttdisplays"] = [serialize(display) for display in d.pop("mqtt_displays")]
                    d["mqttbrokers"] = [serialize(broker) for broker in d.pop("mqtt_brokers")]
                    d["mqttsensors"] = [serialize(sensor) for sensor in d.pop("mqtt_sensors")]

                if isinstance(obj, Info):
                    d["id"] = d.pop("device_id")
                    d["mac"] = d.pop("mac")
                    d["ipaddress"] = d.pop("ip_address")
                    d["firmware"] = d.pop("firmware")
                    d["largedisplay"] = d.pop("large_display")
                    d["connectors"] = [serialize(connector) for connector in d.pop("connectors")]
                    d["sensors"] = [serialize(sensor) for sensor in d.pop("sensors")]

                elif isinstance(obj, Connector):
                    d["id"] = d.pop("connector_id")
                    d["type"] = d.pop("connector_type")

                elif isinstance(obj, Sensor):
                    d["sensorid"] = d.pop("sensor_id")
                    d["description"] = d.pop("description")

                elif isinstance(obj, Core):
                    d["name"] = d.pop("name")
                    d["location"] = d.pop("location")
                    d["autobackup"] = d.pop("auto_backup")
                    d["brightness"] = d.pop("brightness")
                    d["color"] = d.pop("color")
                    d["statusbar"] = d.pop("statusbar")
                    d["topics"] = [serialize(topic) for topic in d.pop("topics")]

                elif isinstance(obj, MqttButton):
                    d["id"] = d.pop("button_id")
                    d["label"] = d.pop("label")
                    d["toplabel"] = d.pop("top_label")
                    d["ledcolorfront"] = d.pop("led_color_front")
                    d["ledcolorwall"] = d.pop("led_color_wall")
                    d["longdelay"] = d.pop("long_delay")
                    d["longrepeat"] = d.pop("long_repeat")
                    d["topics"] = [serialize(topic) for topic in d.pop("topics")]

                elif isinstance(obj, Topic):
                    d["brokerid"] = d.pop("broker_id")
                    d["topic"] = d.pop("topic")
                    d["payload"] = d.pop("payload")
                    d["eventtype"] = d.pop("event_type")

                elif isinstance(obj, MqttDisplay):
                    d["x"] = d.pop("x")
                    d["y"] = d.pop("y")
                    d["boxtype"] = d.pop("box_type")
                    d["fontsize"] = d.pop("font_size")
                    d["align"] = d.pop("align")
                    d["width"] = d.pop("width")
                    d["label"] = d.pop("label")
                    d["unit"] = d.pop("unit")
                    d["round"] = d.pop("round")
                    d["page"] = d.pop("page")
                    d["topics"] = [serialize(topic) for topic in d.pop("topics")]

                elif isinstance(obj, MqttBroker):
                    d["brokerid"] = d.pop("broker_id")
                    d["url"] = d.pop("url")
                    d["port"] = d.pop("port")
                    d["wsport"] = d.pop("ws_port")
                    d["username"] = d.pop("username")
                    d["password"] = d.pop("password")

                elif isinstance(obj, MqttSensor):
                    d["sensorid"] = d.pop("sensor_id")
                    d["interval"] = d.pop("interval")
                    d["topic"] = serialize(d["topic"])

                return {k: v for k, v in d.items() if v is not None}
            else:
                return str(obj)

        return json.dumps(self, default=serialize)

