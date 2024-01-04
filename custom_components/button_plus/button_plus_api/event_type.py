from enum import Enum


class EventType(int, Enum):
    CLICK = 0
    LONG_PRESS = 1
    BLUE_LED = 8
    RED_LED = 9
    GREEN_LED = 10
    LABEL = 11
    TOPLABEL = 12
    RGB_LED = 13
    LED = 14
    VALUE = 15
    UNIT = 17
    SENSOR_VALUE = 18
