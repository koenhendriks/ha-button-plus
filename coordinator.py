from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


class ButtonPlusCoordinator(DataUpdateCoordinator):
    """Button Plus coordinator."""

    async def _async_update_data(self):
        """Fetch data from MQTT subscriptions
        """


