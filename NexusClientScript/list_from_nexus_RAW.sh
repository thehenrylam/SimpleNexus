#!/bin/bash

. ./client_config.sh

get_html_output() {
	NEXUS_FILE_PATH=$1
	NEXUS_FILE_PATH="${NEXUS_FILE_PATH#\/}"
	NEXUS_FILE_PATH="${NEXUS_FILE_PATH%\/}"

	curl -u "$(cat ${AUTH_TOKEN_FILE})" \
		-X 'GET' \
		"${NEXUS_URL}/service/rest/repository/browse/${REPO_NAME_RAW}/${NEXUS_FILE_PATH}/" \
		-H 'X-Nexus-UI: true' \
		2>/dev/null
}	

NEXUS_FILE_PATH=$1
get_html_output ${NEXUS_FILE_PATH} | grep -s "${NEXUS_URL}" | grep -o 'href="[^"]*' | sed 's/href="//' 
exit $?



