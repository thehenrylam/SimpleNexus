#!/bin/bash

. ./client_config.sh

REPO_FILE_PATH="$1"
CURR_FILE_PATH="$2"
NEXUS_URL="http://${NEXUS_IP_ADDRESS}:8081"
FULL_URL_PATH="${NEXUS_URL}/repository/${REPO_NAME_MVN}/${REPO_FILE_PATH}"

echo "OPERATION SUMMARY"
echo "PULL : $(readlink -f ${CURR_FILE_PATH}) <- ${FULL_URL_PATH}"

wget --no-verbose \
  --user=$(grep -Go '^[^:]*' ${AUTH_TOKEN_FILE}) \
  --password=$(grep -Go '[^:]*$' ${AUTH_TOKEN_FILE}) \
  "${FULL_URL_PATH}" -O ${CURR_FILE_PATH}

exit $?

