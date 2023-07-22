#!/bin/bash

. ./app_config.sh

echo "Stopping ${KEYWORD} Container"

docker stop --time=120 ${CONTAINER_NAME}

