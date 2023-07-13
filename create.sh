#!/bin/bash

. ./app_config.sh

echo "Creating Pulp Container"

docker build -t ${IMAGE_NAME} .

docker create --name ${CONTAINER_NAME} \
  --restart=on-failure \
  -p 8080:80 \
  -v "$(pwd)/settings":/etc/pulp \
  -v "$(pwd)/pulp_storage":/var/lib/pulp \
  -v "$(pwd)/pgsql":/var/lib/pgsql \
  -v "$(pwd)/containers":/var/lib/containers \
  --device /dev/fuse \
  pulp/pulp

