#!/bin/bash

. ./app_config.sh

echo "Creating ${KEYWORD} Container"

# docker build -t ${IMAGE_NAME} .

docker create --name ${CONTAINER_NAME} \
  --restart=on-failure \
  -p 8081:8081 \
  -v ${VOLUME_NAME}:/nexus-data \
  "${DOCKER_IMAGE}"

