import pytest
from custom_components.button_plus.button_plus_api.model_detection import ModelDetection
from custom_components.button_plus.button_plus_api.model_v1_07 import (
    DeviceConfiguration as DeviceConfiguration_v1_07,
)
from custom_components.button_plus.button_plus_api.model_v1_12 import (
    DeviceConfiguration as DeviceConfiguration_v1_12,
)


@pytest.fixture
def json_data_v1_07():
    with open("resource/physicalconfig1.07.json") as file:
        return file.read()


@pytest.fixture
def json_data_v1_12():
    with open("resource/physicalconfig1.12.1.json") as file:
        return file.read()


def test_model_for_json_v1_07(json_data_v1_07):
    device_config = ModelDetection.model_for_json(json_data_v1_07)
    assert isinstance(device_config, DeviceConfiguration_v1_07)


def test_model_for_json_v1_12(json_data_v1_12):
    device_config = ModelDetection.model_for_json(json_data_v1_12)
    assert isinstance(device_config, DeviceConfiguration_v1_12)
