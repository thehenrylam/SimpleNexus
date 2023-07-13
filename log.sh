#!/bin/bash

. ./app_config.sh

echo "Opening Logs of ${KEYWORD} Container"

docker logs ${CONTAINER_NAME}

