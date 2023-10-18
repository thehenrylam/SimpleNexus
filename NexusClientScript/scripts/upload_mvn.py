#!/bin/python3

import sys
import os
import re
import subprocess

import standard_utils
from shell_utils import Shell

CLIENT_CONFIG_FILE="./client_config.yml" 
CLIENT_CONFIG=dict()
TARGET_REPO=None

# Get the filename extension from the string
def get_filename_extension(string, delimiter='.'):
    # Get a list of indices of string that match the delimiter
    list_of_indices = [ i for i, c in enumerate(string) if c == delimiter ]
    # If the list of indices is empty, then output empty string (i.e. no valid extension found)
    if (len(list_of_indices) == 0):
        return ""
    # Get the last index of the list of indices
    last_index = list_of_indices[-1]
    # Get the filename extension 
    filename_extension = string[last_index+1:]
    return filename_extension

# Upload the file to the maven repository
def upload_file_to_mvn(local_filepath, group_id, artifact_id, version_id):
    NEXUS_URL = CLIENT_CONFIG["nexus_url"]
    REPO_NAME = CLIENT_CONFIG["repo_name"][ TARGET_REPO ]
    AUTH_TOKEN_FILE = CLIENT_CONFIG["auth_token_file"]

    asset_filepath = local_filepath
    asset_extension = get_filename_extension(local_filepath)
    packaging_type = "jar"
    generate_pom = "true"

    full_filepath = Shell.readlink(local_filepath)

    print("OPERATION SUMMARY")
    print("PUSH : {full_filepath} -> {nexus_url} {group_id}.{artifact_id}.{packaging_type} v{version_id}".format(
        full_filepath=full_filepath, 
        nexus_url=NEXUS_URL, 
        group_id=group_id, 
        artifact_id=artifact_id, 
        packaging_type=packaging_type, 
        version_id=version_id
    ))

    # Initialize the upload command and execute it
    upload_cmd_list = [
        "curl -u $(cat {auth_token_file}) ".format(auth_token_file=AUTH_TOKEN_FILE),
        "-X 'POST' ", 
        "{nexus_url}/service/rest/v1/components?repository={repo_name_mvn} ".format(nexus_url=NEXUS_URL, repo_name_mvn=REPO_NAME),
        "-F \"maven2.groupId={}\" ".format(group_id),
		"-F \"maven2.artifactId={}\" ".format(artifact_id),
		"-F \"maven2.version={}\" ".format(version_id),
		"-F \"maven2.generate-pom={}\" ".format(generate_pom),
		"-F \"maven2.asset1=@{}\" ".format(asset_filepath),
		"-F \"maven2.asset1.extension={}\" ".format(asset_extension),
        "2> /dev/null "
    ]
    upload_cmd = " ".join(upload_cmd_list)
    upload_prc = subprocess.run([upload_cmd], shell=True, stdout=subprocess.PIPE)
    upload_out = upload_prc.stdout.decode('utf-8')

    print(upload_out)

    # If the repository reports it 'does not allow updating assets', 
    # then set the exit code to 2 (not an typical result, but not a failure)
    pattern = re.compile("Repository does not allow updating assets")
    rgx_result = pattern.search(upload_out)
    if (rgx_result != None):
        return 2

    return 0

def help_message():
    print("USAGE: {} <TARGET_REPO> <LOCAL_FILEPATH> <GROUP_ID> <ARTIFACT_ID> <VERSION_ID>".format(sys.argv[0]))
    return

if __name__ == "__main__":
    mandatory_arguments = []
    try:
        (mandatory_arguments, _) = standard_utils.get_arguments( sys.argv, 5 )
    except ValueError:
        help_message()
        exit(1)
    [_, TARGET_REPO, local_filepath, group_id, artifact_id, version_id] = mandatory_arguments

    CLIENT_CONFIG = standard_utils.initialize_configs_from_file( CLIENT_CONFIG_FILE ) 

    exit_code = upload_file_to_mvn(local_filepath, group_id, artifact_id, version_id)
    # print("exit {}".format(exit_code))
    exit(exit_code)
