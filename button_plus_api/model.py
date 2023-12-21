import json
from typing import List, Dict, Any


class Connector:
    def __init__(self, connector_id: int, connector_type: int):
        self.connector_id = connector_id
        self.connector_type = connector_type


class Sensor:
    def __init__(self, sensor_id: int, description: str):
        self.sensor_id = sensor_id
        self.description = description


class Info:
    def __init__(self, device_id: str, mac: str, ip_address: str, firmware: str, large_display: int,
                 connectors: List[Dict[str, Any]], sensors: List[Dict[str, Any]]):
        self.device_id = device_id
        self.mac = mac
        self.ip_address = ip_address
        self.firmware = firmware
        self.large_display = large_display
        self.connectors = [Connector(**connector) for connector in connectors]
        self.sensors = [Sensor(**sensor) for sensor in sensors]


class Core:
    def __init__(self, name: str, location: str, invert: bool, auto_backup: bool, brightness_large_display: int,
                 brightness_mini_display: int, led_color_front: int, led_color_wall: int, color: int):
        self.name = name
        self.location = location
        self.invert = invert
        self.auto_backup = auto_backup
        self.brightness_large_display = brightness_large_display
        self.brightness_mini_display = brightness_mini_display
        self.led_color_front = led_color_front
        self.led_color_wall = led_color_wall
        self.color = color


class MqttButton:
    def __init__(self, button_id: int, label: str, top_label: str, led_color_front: int, led_color_wall: int,
                 topics: List[Dict[str, Any]]):
        self.button_id = button_id
        self.label = label
        self.top_label = top_label
        self.led_color_front = led_color_front
        self.led_color_wall = led_color_wall
        self.topics = topics


class Topic:
    def __init__(self, broker_id: str, topic: str, payload: str, event_type: int):
        self.broker_id = broker_id
        self.topic = topic
        self.payload = payload
        self.event_type = event_type


class MqttDisplay:
    def __init__(self, x: int, y: int, font_size: int, align: int, width: int, label: str, unit: str, round: int,
                 topics: List[Dict[str, Any]]):
        self.x = x
        self.y = y
        self.font_size = font_size
        self.align = align
        self.width = width
        self.label = label
        self.unit = unit
        self.round = round
        self.topics = [Topic(**topic) for topic in topics]


class MqttBroker:
    def __init__(self, broker_id: str, url: str, port: int, ws_port: int):
        self.broker_id = broker_id
        self.url = url
        self.port = port
        self.ws_port = ws_port


class MqttSensor:
    def __init__(self, sensor_id: int, topic: Dict[str, Any], interval: int):
        self.sensor_id = sensor_id
        self.topic = Topic(**topic)
        self.interval = interval


class DeviceConfiguration:
    def __init__(self, info: Dict[str, Any], core: Dict[str, Any], mqtt_buttons: List[Dict[str, Any]],
                 mqtt_displays: List[Dict[str, Any]], mqtt_brokers: List[Dict[str, Any]],
                 mqtt_sensors: List[Dict[str, Any]]):
        self.info = Info(**info)
        self.core = Core(**core)
        self.mqtt_buttons = [MqttButton(**button) for button in mqtt_buttons]
        self.mqtt_displays = [MqttDisplay(**display) for display in mqtt_displays]
        self.mqtt_brokers = [MqttBroker(**broker) for broker in mqtt_brokers]
        self.mqtt_sensors = [MqttSensor(**sensor) for sensor in mqtt_sensors]

    @staticmethod
    def from_json(json_data: str) -> 'DeviceConfiguration':
        """ Parses a JSON string representing the device configuration """
        data = json.loads(json_data)
        return DeviceConfiguration(**data)

    def to_json(self) -> str:
        """ Converts the DeviceConfiguration instance back into a JSON string. """

        def serialize(obj):
            """
            A helper function for json.dumps to serialize custom objects.
            """
            if hasattr(obj, '__dict__'):
                return obj.__dict__
            else:
                return str(obj)

        return json.dumps(self, default=serialize, indent=4)
