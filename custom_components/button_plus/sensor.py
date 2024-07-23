"""Platform for sensor integration."""
# This file shows the setup for the sensors associated with the cover.
# They are setup in the same way with the call to the async_setup_entry function
# via HA from the module __init__. Each sensor has a device_class, this tells HA how
# to display it in the UI (for know types). The unit_of_measurement property tells HA
# what the unit is, so it can display the correct range. For predefined types (such as
# battery), the unit_of_measurement should match what's expected.

from homeassistant.const import (
    DEVICE_CLASS_ILLUMINANCE,
)
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from .buttonplushub import ButtonPlusBase
from .const import DOMAIN


# See cover.py for more details.
# Note how both entities for each roller sensor (battry and illuminance) are added at
# the same time to the same list. This way only a single async_add_devices call is
# required.
async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    new_devices = []
    for device in hub.devices:
        new_devices.append(IlluminanceSensor(device))

    if new_devices:
        async_add_entities(new_devices)


# This base class shows the common properties and methods for a sensor as used in this
# example. See each sensor for further details about properties and methods that
# have been overridden.
class SensorBase(Entity):
    """Base representation of a Button+ Sensor."""

    should_poll = False

    def __init__(self, buttonplus_base):
        """Initialize the sensor."""
        self._base = buttonplus_base

    # To link this entity to the cover device, this property must return an
    # identifiers value matching that used in the cover, but no other information such
    # as name. If name is returned, this entity will then also become a device in the
    # HA UI.
    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._base.button_plus_base_id)},
            # If desired, the name for the device could be different to the entity
            "name": self._base.name,
            "sw_version": self._base.firmware_version,
            "model": self._base.model,
            "manufacturer": self._base.hub.manufacturer,
        }

    # This property is important to let HA know if this entity is online or not.
    # If an entity is offline (return False), the UI will refelect this.
    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return self._base.online and self._base.hub.online @ property

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        # Sensors should also register callbacks to HA when their state changes
        self._base.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        # The opposite of async_added_to_hass. Remove any registered call backs here.
        self._base.remove_callback(self.async_write_ha_state)


# This is another sensor, but more simple compared to the battery above. See the
# comments above for how each field works.
class IlluminanceSensor(SensorBase):
    """Representation of a Sensor."""

    device_class = DEVICE_CLASS_ILLUMINANCE
    _attr_unit_of_measurement = "lx"

    def __init__(self, buttonplus_base=ButtonPlusBase):
        """Initialize the sensor."""
        super().__init__(buttonplus_base)
        # As per the sensor, this must be a unique value within this domain. This is done
        # by using the device ID, and appending "_battery"
        self._attr_unique_id = f"{self._base.button_plus_base_id}_illuminance"

        # The name of the entity
        self._attr_name = f"{self._base.name} Illuminance"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._base.illuminance
