"""Config flow for Hello World integration."""

from __future__ import annotations

import ipaddress
import json
import logging
import traceback
from json import JSONDecodeError

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_IP_ADDRESS, CONF_EMAIL, CONF_PASSWORD
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.network import get_url
from packaging import version

from .button_plus_api.api_client import ApiClient
from .button_plus_api.local_api_client import LocalApiClient
from .button_plus_api.model import ConnectorEnum, DeviceConfiguration, MqttBroker
from .button_plus_api.event_type import EventType
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Button+."""

    local_brokers = ["core-mosquitto", "127.0.0.1", "localhost"]

    def __init__(self):
        self.mqtt_entry = None
        self.broker_endpoint = None

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial Button+ setup, showing the 2 options and checking the MQTT integration."""
        errors = {}
        mqtt_entries = self.hass.config_entries.async_entries(domain="mqtt")

        if len(mqtt_entries) < 1:
            mqtt_url = f"{get_url(self.hass)}/config/integrations/integration/mqtt"

            return self.async_abort(
                reason="mqtt_not_enabled",
                description_placeholders={"mqtt_integration_link": mqtt_url},
            )

        mqtt_entry = mqtt_entries[0]
        broker = self.get_mqtt_endpoint(mqtt_entry.data.get("broker"))
        broker_port = mqtt_entry.data.get("port")
        broker_username = mqtt_entry.data.get("username", "(No authentication)")
        self.mqtt_entry = mqtt_entry

        if user_input is not None:
            self.broker_endpoint = user_input.get("broker", broker)
            return await self.async_step_choose_entry()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required("broker", default=broker): str}),
            errors=errors,
            description_placeholders={
                "mqtt_broker": broker,
                "mqtt_broker_port": broker_port,
                "mqtt_user": broker_username,
            },
        )

    async def async_step_choose_entry(self, user_input=None):
        # if user_input is not None:
        return self.async_show_menu(
            step_id="choose_entry",
            menu_options=["fetch_website", "manual"],
            description_placeholders={},
        )

    async def async_step_manual(self, user_input=None):
        """Handle setting up button plus from manual IP."""
        errors = {}
        ip = None
        if user_input is not None:
            ip = user_input.get(CONF_IP_ADDRESS, None)
            valid = self.validate_ip(ip)
            if valid:
                try:
                    _LOGGER.debug(f"Fetching button+ device at {ip}")
                    api_client = LocalApiClient(
                        ip, aiohttp_client.async_get_clientsession(self.hass)
                    )
                    json_config = await api_client.fetch_config()
                    device_config: DeviceConfiguration = DeviceConfiguration.from_json(
                        json_config
                    )

                    self.add_broker_to_config(device_config)
                    self.add_topics_to_core(device_config)
                    self.add_topics_to_buttons(device_config)

                    await api_client.push_config(device_config)

                    return self.async_create_entry(
                        title=f"{device_config.core.name}",
                        description=f"Base module on {ip} with id {device_config.info.device_id}",
                        data={"config": json_config},
                    )

                except JSONDecodeError as ex:  # pylint: disable=broad-except
                    _LOGGER.error(
                        f"{DOMAIN} Could not parse json from IP {ip} : %s - traceback: %s",
                        ex,
                        traceback.format_exc(),
                    )

                    errors["base"] = f"Error connecting or reading from {ip}"
                except Exception as ex:  # pylint: disable=broad-except
                    _LOGGER.error(
                        f"{DOMAIN} Exception in login : %s - traceback: %s",
                        ex,
                        traceback.format_exc(),
                    )

                    errors["base"] = "cannot_connect"

            else:
                errors["base"] = "invalid_ip"

        return self.async_show_form(
            step_id="manual",
            data_schema=vol.Schema({CONF_IP_ADDRESS: str}),
            errors=errors,
            description_placeholders={"ip": ip},
        )

    async def async_step_fetch_website(self, user_input=None):
        """Handle fetching the Button+ devices from the website."""
        errors = {}

        _LOGGER.debug(f"Fetch website step {user_input}")

        if user_input is not None:
            try:
                api_client = await self.setup_api_client(user_input)

                valid = await api_client.test_connection()

                if valid:
                    json_response = await api_client.fetch_configs()
                    devices = json.loads(json_response)
                    last_entry = None

                    total_devices = len(devices)
                    _LOGGER.info(f"Found {total_devices} devices from Button+ website")

                    for device in devices:
                        device_website_id = device.get("Id")
                        device_ip = device.get("IpAddress")

                        if not device_ip:
                            _LOGGER.warning(
                                f"Skipping device {device_website_id}, it has no IP so must be virtual"
                            )
                            continue

                        _LOGGER.debug(
                            f"loaded device from website with id: {device_website_id} and ip {device_ip}"
                        )
                        device_config = json.loads(device.get("Json"))
                        device_name = device_config.get("core").get("name")
                        device_id = device_config.get("info").get("id")
                        last_entry = self.async_create_entry(
                            title=f"{device_name}",
                            description=f"Base module on {device_ip} with local id {device_id} and website id {device_website_id}",
                            data=device_config,
                        )

                    return last_entry

            except JSONDecodeError as ex:  # pylint: disable=broad-except
                _LOGGER.error(
                    f"{DOMAIN}  Could not parse json from Button+ website : %s - traceback: %s",
                    ex,
                    traceback.format_exc(),
                )

                errors["base"] = (
                    "Error connecting or reading from https://api.button.plus/"
                )
            except Exception as ex:  # pylint: disable=broad-except
                _LOGGER.error(
                    f"{DOMAIN} Exception in login : %s - traceback: %s",
                    ex,
                    traceback.format_exc(),
                )

                errors["base"] = "cannot_connect"

            if "base" not in errors:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="fetch_website",
            data_schema=vol.Schema(
                {CONF_EMAIL: str, CONF_PASSWORD: str, "cookie": str}
            ),
            errors=errors,
        )

    async def setup_api_client(self, user_input):
        _LOGGER.debug(f"Setting up API client with {user_input}")

        if "cookie" not in user_input:
            client = ApiClient(aiohttp_client.async_get_clientsession(self.hass))
            cookie = await client.get_cookie_from_login(
                user_input.get("email"), user_input.get("password")
            )
        else:
            cookie = user_input.get("cookie")

        return ApiClient(aiohttp_client.async_get_clientsession(self.hass), cookie)

    def validate_ip(self, ip) -> bool:
        try:
            ipaddress.IPv4Address(ip)
            return True
        except ValueError:
            return False

    def add_broker_to_config(
        self, device_config: DeviceConfiguration
    ) -> DeviceConfiguration:
        mqtt_entry = self.mqtt_entry
        broker_port = mqtt_entry.data.get("port")
        broker_username = mqtt_entry.data.get("username", "")
        broker_password = mqtt_entry.data.get("password", "")

        broker = MqttBroker(
            broker_id="ha-button-plus",
            url=f"mqtt://{self.broker_endpoint}/",
            port=broker_port,
            ws_port=9001,
            username=broker_username,
            password=broker_password,
        )

        device_config.mqtt_brokers.append(broker)
        return device_config

    def add_topics_to_core(
        self, device_config: DeviceConfiguration
    ) -> DeviceConfiguration:
        device_id = device_config.info.device_id
        min_version = "1.11"

        if version.parse(device_config.info.firmware) < version.parse(min_version):
            _LOGGER.debug(
                f"Current version {device_config.info.firmware} doesn't support the brightness, it must be at least firmware version {min_version}"
            )
            return

        device_config.core.topics.append(
            {
                "brokerid": "ha-button-plus",
                "topic": f"buttonplus/{device_id}/brightness/large",
                "payload": "",
                "eventtype": EventType.BRIGHTNESS_LARGE_DISPLAY,
            }
        )

        device_config.core.topics.append(
            {
                "brokerid": "ha-button-plus",
                "topic": f"buttonplus/{device_id}/brightness/mini",
                "payload": "",
                "eventtype": EventType.BRIGHTNESS_MINI_DISPLAY,
            }
        )

        device_config.core.topics.append(
            {
                "brokerid": "ha-button-plus",
                "topic": f"buttonplus/{device_id}/page/status",
                "payload": "",
                "eventtype": EventType.PAGE_STATUS,
            }
        )

        device_config.core.topics.append(
            {
                "brokerid": "ha-button-plus",
                "topic": f"buttonplus/{device_id}/page/set",
                "payload": "",
                "eventtype": EventType.SET_PAGE,
            }
        )

    def add_topics_to_buttons(
        self, device_config: DeviceConfiguration
    ) -> DeviceConfiguration:
        device_id = device_config.info.device_id

        active_connectors = [
            connector.connector_id
            for connector in device_config.info.connectors
            if connector.connector_type_enum()
            in [ConnectorEnum.DISPLAY, ConnectorEnum.BAR]
        ]

        for button in filter(
            lambda b: b.button_id // 2 in active_connectors, device_config.mqtt_buttons
        ):
            # Create topics for button main label
            button.topics.append(
                {
                    "brokerid": "ha-button-plus",
                    "topic": f"buttonplus/{device_id}/button/{button.button_id}/label",
                    "payload": "",
                    "eventtype": EventType.LABEL,
                }
            )

            # Create topics for button top label
            button.topics.append(
                {
                    "brokerid": "ha-button-plus",
                    "topic": f"buttonplus/{device_id}/button/{button.button_id}/top_label",
                    "payload": "",
                    "eventtype": EventType.TOPLABEL,
                }
            )

            # Create topics for button click
            button.topics.append(
                {
                    "brokerid": "ha-button-plus",
                    "topic": f"buttonplus/{device_id}/button/{button.button_id}/click",
                    "payload": "press",
                    "eventtype": EventType.CLICK,
                }
            )

            # Create topics for button click
            button.topics.append({
                "brokerid": "ha-button-plus",
                "topic": f"buttonplus/{device_id}/button/{button.button_id}/long_press",
                "payload": "press",
                "eventtype": EventType.LONG_PRESS
            })

        return device_config

    def get_mqtt_endpoint(self, endpoint: str) -> str:
        # Internal add-on is not reachable from the Button+ device so we use the hass ip
        if endpoint in self.local_brokers:
            _LOGGER.debug(
                f"mqtt host is internal so use {self.hass.config.api.host} instead of {endpoint}"
            )
            return self.hass.config.api.host
        return endpoint
