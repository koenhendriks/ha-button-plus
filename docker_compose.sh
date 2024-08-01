#! /bin/bash

## Testing
# You can start a mosquitto broker and Home Assistant with this integration in it with Docker Compose.
# Make sure Docker is installed and run the `docker_compose.sh` script. This script will completely reset
# the docker image every time, making sure there is a clean environment.
#
# When you run the script, after a while:
# - A browser window will open, if not, browse to http://localhost:8123.
# - Setup Home Assistant with a user and location.
# - Add the MQTT integration, use hostname `mosquitto` (no user/pw required).
# - Add the Button+ integration to test, the MQTT broker should be prefilled.
# - Your terminal will attach to the Home Assistant docker, showing you logs
# - Detach with CTRL + C, the docker images will automatically be stopped.
#
# **Note:** This will allow you to setup a real Button+ device and see if setup works.
# Actual communication with the device will not work unless the broker is reachable from Button+.

docker compose down

rm -rf ha_config/*
rm -rf ha_config/.*

cat > ha_config/configuration.yaml<< EOF
logger:
  default: debug
  logs:
    custom_components.button_plus: debug
EOF

docker compose up -d
sleep 1
open "http://localhost:8123/"
docker compose attach homeassistant # This blocks until you detach with CTRL + C

docker compose down
