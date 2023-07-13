#!/bin/bash

. ./app_config.sh

echo "Start ${KEYWORD} Container"

docker start ${CONTAINER_NAME}

