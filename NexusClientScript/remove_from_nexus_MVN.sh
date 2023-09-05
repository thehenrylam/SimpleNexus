#!/bin/bash

. ./client_config.sh

REPO_FILE_PATH="$1"
NEXUS_URL="http://${NEXUS_IP_ADDRESS}:8081"
FULL_URL_PATH="${NEXUS_URL}/repository/${REPO_NAME_MVN}/${REPO_FILE_PATH}"

echo "OPERATION SUMMARY"
echo "REMOVE : ${FULL_URL_PATH}"

api_delete_folder() {
	FOLDER_PATH="$1"

	LIST_OF_FILES=$(./list_from_nexus_MVN.sh)
	TARGET_FILES=$(echo "${LIST_OF_FILES}" | grep -s "${FOLDER_PATH}")
	
	while IFS= read -r file_line; do
		api_delete_file "${file_line}"
	done <<< "${TARGET_FILES}"
}

api_delete_file() {
	FCN_REPO_FILE_PATH="$1"

	FCN_FULL_URL_PATH="${NEXUS_URL}/repository/${REPO_NAME_MVN}/${FCN_REPO_FILE_PATH}"

	curl -v -u $(cat ${AUTH_TOKEN_FILE}) \
		-X "DELETE" \
		"${FCN_FULL_URL_PATH}"
}

if [ "${REPO_FILE_PATH: -1}" = "/" ]; then
	api_delete_folder "${REPO_FILE_PATH}"
else
	api_delete_file "${REPO_FILE_PATH}"	
fi

exit $?

