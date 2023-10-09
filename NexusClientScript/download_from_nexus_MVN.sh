#!/bin/bash

. ./client_config.sh

FULL_URL_PATH=$(echo "$1" | grep -s ${NEXUS_URL})
CURR_FILE_PATH="$2"

echo "OPERATION SUMMARY"
echo "PULL : $(readlink -f ${CURR_FILE_PATH}) <- ${FULL_URL_PATH}"

wget --no-verbose \
  --user=$(grep -Go '^[^:]*' ${AUTH_TOKEN_FILE}) \
  --password=$(grep -Go '[^:]*$' ${AUTH_TOKEN_FILE}) \
  "${FULL_URL_PATH}" -O ${CURR_FILE_PATH}

exit $?

