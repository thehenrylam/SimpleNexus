#!/bin/bash

. ./client_config.sh

FULL_URL_PATH=$(echo "$1" | grep -s ${NEXUS_URL})

echo "OPERATION SUMMARY"
echo "REMOVE : ${FULL_URL_PATH}"

curl -v -u $(cat ${AUTH_TOKEN_FILE}) \
  -X "DELETE" \
  "${FULL_URL_PATH}"

exit $?

