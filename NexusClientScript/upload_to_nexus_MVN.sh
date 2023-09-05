#!/bin/bash

. ./client_config.sh

CURR_FILE_PATH="$1"
ARTIFACT_ID="$2"
VERSION="$3"

MVN_GROUP_ID="${MVN_DEFAULT_GROUP_ID}"

api_upload() {
	ASSET_FILEPATH="$1"
	ASSET_EXTENSION="${ASSET_FILEPATH##*.}"
	GROUP_ID="$2"
	ARTIFACT_ID="$3"
	VERSION="$4"
	PACKAGING_TYPE="jar"
	GENERATE_POM="true"

	PROCESS_OUTPUT=$(curl -u "$(cat ${AUTH_TOKEN_FILE})" \
		-X 'POST' \
		"http://${NEXUS_IP_ADDRESS}:8081/service/rest/v1/components?repository=${REPO_NAME_MVN}" \
		-F "maven2.groupId=${GROUP_ID}" \
		-F "maven2.artifactId=${ARTIFACT_ID}" \
		-F "maven2.version=${VERSION}" \
		-F "maven2.generate-pom=${GENERATE_POM}" \
		-F "maven2.asset1=@${ASSET_FILEPATH}" \
		-F "maven2.asset1.extension=${ASSET_EXTENSION}") 
	CHECK_IS_FILE_UPDATE=$(echo ${PROCESS_OUTPUT} | grep -is "Repository does not allow updating assets")

	echo ${PROCESS_OUTPUT}

	if [ -n "${CHECK_IS_FILE_UPDATE}" ]; then
		exit 2
	fi

}

api_upload "${CURR_FILE_PATH}" "${MVN_GROUP_ID}" "${ARTIFACT_ID}" "${VERSION}"

exit $?


