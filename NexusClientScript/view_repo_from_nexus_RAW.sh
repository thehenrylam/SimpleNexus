#!/bin/bash

. ./client_config.sh

curl -u "$(cat ${AUTH_TOKEN_FILE})" \
  -X 'GET' \
  "http://${NEXUS_IP_ADDRESS}:8081/service/rest/v1/assets?repository=${REPO_NAME}" \
  -H 'accept: application/json' \
  -H 'X-Nexus-UI: true' \
  2>/dev/null

echo $?

