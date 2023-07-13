#!/bin/bash

. ./app_config.sh

echo "Starting Bash of ${KEYWORD} Container"

docker exec -it ${CONTAINER_NAME} /bin/bash

