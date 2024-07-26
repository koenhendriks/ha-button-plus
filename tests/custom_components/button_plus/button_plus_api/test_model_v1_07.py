import pytest
import json

from custom_components.button_plus.button_plus_api.model_v1_07 import (
    DeviceConfiguration,
)


def test_model_v1_07_from_to_json_should_be_same():
    # Load the JSON file
    with open("resource/physicalconfig1.07.json") as file:
        json_string = file.read()
        json_data = json.loads(json_string)

    # Parse the JSON data into a DeviceConfiguration object
    device_config = DeviceConfiguration.from_dict(json_data)

    # Serialize the DeviceConfiguration object back into a JSON string
    new_json_string = device_config.to_json()

    # Parse the JSON data into a DeviceConfiguration object
    new_json_data = json.loads(new_json_string)

    # Assert that the JSON data is the same
    assert json_data == new_json_data


@pytest.fixture
def device_config():
    # Load and parse the JSON file
    with open("resource/physicalconfig1.07.json") as file:
        json_data = json.loads(file.read())
        # Parse the JSON data into a DeviceConfiguration object
        return DeviceConfiguration.from_dict(json_data)


def test_buttons(device_config):
    buttons = device_config.mqtt_buttons
    assert len(buttons) == 8
    assert buttons[0].label == "Btn 0"
    assert buttons[0].top_label == "Label"
    assert buttons[0].led_color_front == 0
    assert buttons[0].led_color_wall == 0
    assert buttons[0].long_delay == 75
    assert buttons[0].long_repeat == 15
    assert buttons[2].topics[0].broker_id == "hassdev"
    assert buttons[2].topics[0].topic == "buttonplus/btn_4967c8/bars/2/click"
    assert buttons[2].topics[0].payload == "true"
    assert buttons[2].topics[0].event_type == 0


def test_mqttdisplays(device_config):
    mqttdisplays = device_config.mqtt_displays
    assert len(mqttdisplays) == 2
    assert mqttdisplays[0].x == 0
    assert mqttdisplays[0].y == 0
    assert mqttdisplays[0].font_size == 4
    assert mqttdisplays[0].align == 0
    assert mqttdisplays[0].width == 50
    assert mqttdisplays[0].round == 0
    assert mqttdisplays[0].label == "Amsterdam"
    assert mqttdisplays[0].unit == ""
    assert mqttdisplays[0].topics[0].broker_id == "buttonplus"
    assert mqttdisplays[0].topics[0].topic == "system/datetime/amsterdam"
    assert mqttdisplays[0].topics[0].payload == ""
    assert mqttdisplays[0].topics[0].event_type == 15
    assert mqttdisplays[1].unit == "°C"


def test_mqttbrokers(device_config):
    mqttbrokers = device_config.mqtt_brokers
    assert len(mqttbrokers) == 2
    assert mqttbrokers[0].broker_id == "buttonplus"
    assert mqttbrokers[0].url == "mqtt://mqtt.button.plus"
    assert mqttbrokers[0].port == 0
    assert mqttbrokers[0].ws_port == 0
    assert mqttbrokers[0].username == ""
    assert mqttbrokers[0].password == ""
    assert mqttbrokers[1].broker_id == "hassdev"
    assert mqttbrokers[1].url == "mqtt://192.168.2.16/"
    assert mqttbrokers[1].port == 1883
    assert mqttbrokers[1].ws_port == 9001
    assert mqttbrokers[1].username == "koen"
    assert mqttbrokers[1].password == "koen"


def test_mqttsensors(device_config):
    mqttsensors = device_config.mqtt_sensors
    assert len(mqttsensors) == 1
    assert mqttsensors[0].sensor_id == 1
    assert mqttsensors[0].interval == 10
    assert mqttsensors[0].topic.broker_id == "buttonplus"
    assert mqttsensors[0].topic.topic == "button/btn_4967c8/temperature"
    assert mqttsensors[0].topic.payload == ""
    assert mqttsensors[0].topic.event_type == 18
