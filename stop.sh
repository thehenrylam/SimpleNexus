#!/bin/bash

. ./app_config.sh

echo "Stopping ${KEYWORD} Container"

docker stop ${CONTAINER_NAME}

