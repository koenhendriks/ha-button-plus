#! /bin/bash

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

open "http://localhost:8123/"

docker compose attach homeassistant

docker compose down
