from typing import Dict, Any
import json
from packaging.version import parse as parseSemver, Version as SemverVersion
from .model_interface import DeviceConfiguration

class ModelDetection:
    @staticmethod
    def model_for_json(json_data: str) -> "DeviceConfiguration":
        data = json.loads(json_data)
        deviceVersion = parseSemver(data["info"]["firmware"]);
        if deviceVersion >= parseSemver("1.12.0"):
            from .model_v1_12 import DeviceConfiguration
            return DeviceConfiguration()
        else:
            from .model_v1_07 import DeviceConfiguration
            return DeviceConfiguration()
