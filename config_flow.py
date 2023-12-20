"""Config flow for Hello World integration."""
from __future__ import annotations

import json
import logging
import traceback
from json import JSONDecodeError
from typing import Any

import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client

from .buttonplushub import ButtonPlusHub
from .const import DOMAIN  # pylint:disable=unused-import
from .button_plus_api import ApiClient

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({"cookie": str})


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello World."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self) -> None:
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle the initial Button+ step."""
        return self.async_show_menu(
            step_id="user",
            menu_options=["fetch_website", "manual"],
        )

    async def async_step_fetch_website(self, user_input=None):
        """Handle fetching the Button+ devices from the website."""

        _LOGGER.debug(f"Fetch website step {user_input}")

        if user_input is not None:
            try:
                api_client = ApiClient(user_input['cookie'], aiohttp_client.async_get_clientsession(self.hass))

                valid = await api_client.test_connection()

                if valid:
                    json_response = await api_client.fetch_configs()
                    devices = json.loads(json_response)
                    last_entry = None

                    total_devices = len(devices)
                    _LOGGER.info(f"Found {total_devices} devices from Button+ website")

                    for device in devices:
                        device_website_id = device.get("Id")
                        device_ip = device.get('IpAddress');

                        if not device_ip:
                            _LOGGER.warning(f"Skipping device {device_website_id}, it has no IP so must be virtual")
                            continue

                        _LOGGER.debug(f"loaded device from website with id: {device_website_id} and ip {device_ip}")
                        device_config = json.loads(device.get("Json"))
                        last_entry = self.async_create_entry(
                            title=f"button+ {device_website_id}",
                            description=f"Base module with website id {device_website_id}",
                            data=device_config
                        )

                    return last_entry

            except JSONDecodeError as ex:  # pylint: disable=broad-except
                _LOGGER.error(
                    f"{DOMAIN}  Could not parse json from Button+ website : %s - traceback: %s",
                    ex,
                    traceback.format_exc()
                )

                self._errors["base"] = "Error connecting or reading from https://api.button.plus/"
            except Exception as ex:  # pylint: disable=broad-except
                _LOGGER.error(
                    f"{DOMAIN} Exception in login : %s - traceback: %s",
                    ex,
                    traceback.format_exc()
                )

                self._errors["base"] = "cannot_connect"

            if "base" not in self._errors:
                self._errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="fetch_website",
            data_schema=DATA_SCHEMA,
            errors=self._errors
        )
