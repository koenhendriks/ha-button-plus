from enum import Enum


class ConnectorType(int, Enum):
    NOT_CONNECTED = 0
    BAR = 1
    DISPLAY = 2
