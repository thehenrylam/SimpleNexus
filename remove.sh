#!/bin/bash

. ./app_config.sh

echo "Removing ${KEYWORD} Container"

docker stop ${CONTAINER_NAME}

docker rm ${CONTAINER_NAME}

