from custom_components.button_plus.button_plus_api.model_v1_12 import DeviceConfiguration
import json


def test_model_v1_12_from_to_json_should_be_same():
    # Load the JSON file
    with open('resource/physicalconfig1.12.1.json') as file:
        json_data = json.loads(file.read())

    # Parse the JSON data into a DeviceConfiguration object
    device_config = DeviceConfiguration.from_json(json_data)

    # Serialize the DeviceConfiguration object back into a JSON string
    json_string = device_config.to_json()

    original_json_data = json_data
    new_json_data = json.loads(json_string)

    # Assert that the JSON strings are the same
    assert original_json_data == new_json_data


def test_model_v1_12():
    # Load the JSON file
    with open('resource/physicalconfig1.12.1.json') as file:
        json_data = json.loads(file.read())

    # Parse the JSON data into a DeviceConfiguration object
    device_config = DeviceConfiguration.from_json(json_data)

    # Assert the values from the parsed DeviceConfiguration object
    assert device_config.info.device_id == "btn_4584b8"
    assert device_config.info.mac == "F4:12:FA:45:84:B8"
    assert device_config.info.ip_address == "192.168.102.10"
    assert device_config.info.firmware == "1.12.2"
    assert device_config.info.large_display == 0

    # Assert the values from the parsed Core object
    assert device_config.core.name == "btn_4584b8"
    assert device_config.core.location == "Room 1"
    assert device_config.core.auto_backup == True
    assert device_config.core.brightness == 80
    assert device_config.core.color == 16765791
    assert device_config.core.statusbar == 2

    # Assert the values from the parsed MqttButton objects
    assert len(device_config.mqtt_buttons) == 8
    assert device_config.mqtt_buttons[0].button_id == 0
    assert device_config.mqtt_buttons[0].label == "Btn 0"
    assert device_config.mqtt_buttons[0].top_label == "Label"
    assert device_config.mqtt_buttons[0].led_color_front == 0
    assert device_config.mqtt_buttons[0].led_color_wall == 0
    assert device_config.mqtt_buttons[0].long_delay == 40
    assert device_config.mqtt_buttons[0].long_repeat == 15

    assert device_config.mqtt_buttons[1].button_id == 1
    assert device_config.mqtt_buttons[1].label == "Btn 1"
    assert device_config.mqtt_buttons[1].top_label == "Label"
    assert device_config.mqtt_buttons[1].led_color_front == 0
    assert device_config.mqtt_buttons[1].led_color_wall == 0
    assert device_config.mqtt_buttons[1].long_delay == 40
    assert device_config.mqtt_buttons[1].long_repeat == 15

    # Assert the values from the parsed MqttDisplay objects
    assert len(device_config.mqtt_displays) == 2
    assert device_config.mqtt_displays[0].x == 0
    assert device_config.mqtt_displays[0].y == 0
    assert device_config.mqtt_displays[0].font_size == 4
    assert device_config.mqtt_displays[0].align == 1
    assert device_config.mqtt_displays[0].width == 50
    assert device_config.mqtt_displays[0].label == "Amsterdam"
    assert device_config.mqtt_displays[0].unit == ""
    assert device_config.mqtt_displays[0].round == 0

    # Assert the values from the parsed MqttBroker objects
    assert len(device_config.mqtt_brokers) == 2
    assert device_config.mqtt_brokers[0].broker_id == "ha"
    assert device_config.mqtt_brokers[0].url == "ha.localdomain"
    assert device_config.mqtt_brokers[0].port == 0
    assert device_config.mqtt_brokers[0].ws_port == 0
    assert device_config.mqtt_brokers[0].username == "mqtt_user"
    assert device_config.mqtt_brokers[0].password == "mqtt_password"

    # Assert the values from the parsed MqttSensor objects
    assert len(device_config.mqtt_sensors) == 1
    assert device_config.mqtt_sensors[0].sensor_id == 1
    assert device_config.mqtt_sensors[0].interval == 10
    assert device_config.mqtt_sensors[0].topic.broker_id == "buttonplus"
    assert device_config.mqtt_sensors[0].topic.topic == "button/btn_4584b8/temperature"
    assert device_config.mqtt_sensors[0].topic.payload == ""
    assert device_config.mqtt_sensors[0].topic.event_type == 18
