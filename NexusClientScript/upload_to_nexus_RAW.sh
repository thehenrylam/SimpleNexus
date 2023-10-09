#!/bin/bash

. ./client_config.sh

CURR_FILE_PATH="$1"
REPO_FILE_PATH="$2"
FULL_URL_PATH="${NEXUS_URL}/repository/${REPO_NAME_RAW}/${REPO_FILE_PATH}"

echo "OPERATION SUMMARY"
echo "PUSH : $(readlink -f ${CURR_FILE_PATH}) -> ${FULL_URL_PATH}"

curl -v -u "$(cat ${AUTH_TOKEN_FILE})" --upload-file ${CURR_FILE_PATH} "${FULL_URL_PATH}" 

exit $?

