#!/bin/bash

. ./client_config.sh

REPO_FILE_PATH="$1"
NEXUS_URL="http://${NEXUS_IP_ADDRESS}:8081"
FULL_URL_PATH="${NEXUS_URL}/repository/${REPO_NAME}/${REPO_FILE_PATH}"

echo "OPERATION SUMMARY"
echo "REMOVE : ${FULL_URL_PATH}"

curl -v -u $(cat ${AUTH_TOKEN_FILE}) \
  -X "DELETE" \
  "${FULL_URL_PATH}"

exit $?

