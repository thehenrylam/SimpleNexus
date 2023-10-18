#!/bin/bash


DESTINATION_USERHOST="$1"
DESTINATION_FILEPATH="$2"

CUR_TIMESTAMP=$(date "+%Y%m%d%H%M%S")

NEXUS_FILENAME="NexusClientScript"
NEXUS_FILENAME_BCK="${NEXUS_FILENAME}_bck${CUR_TIMESTAMP}"

# Remove NexusClientScript.tar.gz (if there is any)
rm "${NEXUS_FILENAME}.tar.gz"

# Package the NexusClientScript/ folder into NexusClientScript.tar.gz
tar -cvf "${NEXUS_FILENAME}.tar.gz" "${NEXUS_FILENAME}/" 

# Copy the *.tar.gz file to the destination host and filepath 
scp "${NEXUS_FILENAME}.tar.gz" ${DESTINATION_USERHOST}:${DESTINATION_FILEPATH} 
exit_code=$?
if [ $exit_code -ne 0 ]; then
	echo "ERROR: Unable to copy the ${NEXUS_FILENAME}.tar.gz file to the host and filepath: ${DESTINATION_USERHOST}:${DESTINATION_FILEPATH}"
	exit 1
fi

# In the destination host: Move the NexusClientScript to be archived
CMD_CD_DESTINATION="cd ${DESTINATION_FILEPATH}"
CMD_MV_PREV_NEXUS="mv ${NEXUS_FILENAME} ${NEXUS_FILENAME_BCK}"
CMD_TAR_PREV_NEXUS="tar -cvf ${NEXUS_FILENAME_BCK}.tar.gz ${NEXUS_FILENAME_BCK}/"
CMD_RM_PREV_NEXUS="rm -r ${NEXUS_FILENAME_BCK}/"
CMD_EXPAND_CURR_NEXUS="tar -xvf ${NEXUS_FILENAME}.tar.gz"
CMD_CLEAN_CURR_NEXUS="rm ${NEXUS_FILENAME}.tar.gz"

ssh "${DESTINATION_USERHOST}" "${CMD_CD_DESTINATION} && ${CMD_MV_PREV_NEXUS} && ${CMD_TAR_PREV_NEXUS} && ${CMD_RM_PREV_NEXUS} && ${CMD_EXPAND_CURR_NEXUS} && ${CMD_CLEAN_CURR_NEXUS}"
exit_code=$?
if [ $exit_code -ne 0 ]; then
	echo "ERROR: Unable to execute commands in the host: ${DESTINATION_USERHOST}"
	exit 1
fi

