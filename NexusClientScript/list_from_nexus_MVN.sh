#!/bin/bash

. ./client_config.sh

help() {
	echo "Usage: $0"
	echo "options:"
	echo "	-h : Print this help message."
	echo "	-j : Print the full JSON output from the web query."
}

api_list() {
	curl -u "$(cat ${AUTH_TOKEN_FILE})" \
		-X 'GET' \
		"http://${NEXUS_IP_ADDRESS}:8081/service/rest/v1/components?repository=${REPO_NAME_MVN}" \
		-H 'accept: application/json' \
		-H 'X-Nexus-UI: true' \
		2>/dev/null
}	

while getopts ":hj" option; do
	case $option in 
		h) # display help
			help
			exit 0 
			;;
		j) # Print full json format
			api_list 
			exit $? 
			;;
	esac 
done

api_list | grep -Po "\"path\"[^:]*:[\s]*\"\K([^\"]*)" 
exit $?



