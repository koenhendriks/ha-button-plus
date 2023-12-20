"""Config flow for Hello World integration."""
from __future__ import annotations

import ipaddress
import json
import logging
import traceback
from json import JSONDecodeError

import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.const import CONF_IP_ADDRESS
from homeassistant.helpers import aiohttp_client

from .const import DOMAIN  # pylint:disable=unused-import
from .button_plus_api import ApiClient
from .button_plus_api_local import ApiClient as LocalApiClient

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello World."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial Button+ setup, showing the 2 options."""
        return self.async_show_menu(
            step_id="user",
            menu_options=["fetch_website", "manual"],
        )

    async def async_step_manual(self, user_input=None):
        """ Handle setting up button plus from manual IP."""
        errors = {}
        ip = None
        if user_input is not None:
            ip = user_input.get(CONF_IP_ADDRESS, None)
            valid = self.validate_ip(ip)
            if valid:
                try:
                    _LOGGER.debug(f"Fetching button+ device at {ip}")
                    api_client = LocalApiClient(ip, aiohttp_client.async_get_clientsession(self.hass))
                    json_config = await api_client.fetch_config()
                    config = json.loads(json_config)
                    device_name = config.get('core').get('name')
                    device_id = config.get('info').get('id')

                    _LOGGER.debug(f"Local config found with device {device_name} and id {device_id}")

                    return self.async_create_entry(
                        title=f"{device_name}",
                        description=f"Base module on {ip} with id {device_id}",
                        data=config
                    )

                except JSONDecodeError as ex:  # pylint: disable=broad-except
                    _LOGGER.error(
                        f"{DOMAIN}  Could not parse json from IP {ip} : %s - traceback: %s",
                        ex,
                        traceback.format_exc()
                    )

                    errors["base"] = "Error connecting or reading from {ip}"
                except Exception as ex:  # pylint: disable=broad-except
                    _LOGGER.error(
                        f"{DOMAIN} Exception in login : %s - traceback: %s",
                        ex,
                        traceback.format_exc()
                    )

                    errors["base"] = "cannot_connect"

            else:
                errors["base"] = 'invalid_ip'

        return self.async_show_form(
            step_id="manual",
            data_schema=vol.Schema({CONF_IP_ADDRESS: str}),
            errors=errors,
            description_placeholders={
                "ip": ip
            }
        )

    async def async_step_fetch_website(self, user_input=None):
        """Handle fetching the Button+ devices from the website."""
        errors = {}

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
                        device_ip = device.get('IpAddress')

                        if not device_ip:
                            _LOGGER.warning(f"Skipping device {device_website_id}, it has no IP so must be virtual")
                            continue

                        _LOGGER.debug(f"loaded device from website with id: {device_website_id} and ip {device_ip}")
                        device_config = json.loads(device.get("Json"))
                        device_name = device_config.get('core').get('name')
                        device_id = device_config.get('info').get('id')
                        last_entry = self.async_create_entry(
                            title=f"{device_name}",
                            description=f"Base module on {device_ip} with local id {device_id} adn website id {device_website_id}",
                            data=device_config
                        )

                    return last_entry

            except JSONDecodeError as ex:  # pylint: disable=broad-except
                _LOGGER.error(
                    f"{DOMAIN}  Could not parse json from Button+ website : %s - traceback: %s",
                    ex,
                    traceback.format_exc()
                )

                errors["base"] = "Error connecting or reading from https://api.button.plus/"
            except Exception as ex:  # pylint: disable=broad-except
                _LOGGER.error(
                    f"{DOMAIN} Exception in login : %s - traceback: %s",
                    ex,
                    traceback.format_exc()
                )

                errors["base"] = "cannot_connect"

            if "base" not in errors:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="fetch_website",
            data_schema=vol.Schema({"cookie": str}),
            errors=errors
        )

    def validate_ip(self, ip) -> bool:
        try:
            ipaddress.IPv4Address(ip)
            return True
        except ValueError:
            return False
