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
def upload_file_to_mvn(local_filepath, nexus_filepath):
    NEXUS_URL = CLIENT_CONFIG["nexus_url"]
    REPO_NAME = CLIENT_CONFIG["repo_name"][ TARGET_REPO ]
    AUTH_TOKEN_FILE = CLIENT_CONFIG["auth_token_file"]

    full_filepath = Shell.readlink(local_filepath)
    full_urlpath = "{nexus_url}/repository/{repo_name}/{nexus_filepath}".format(nexus_url=NEXUS_URL, repo_name=REPO_NAME, nexus_filepath=nexus_filepath)

    print("OPERATION SUMMARY")
    print("PUSH : {full_filepath} -> {full_urlpath}".format(full_filepath=full_filepath, full_urlpath=full_urlpath))

    # Initialize the upload command and execute it
    upload_cmd = "curl -u $(cat {auth_token_file}) --upload-file {full_filepath} \"{full_urlpath}\" 2> /dev/null".format(
        auth_token_file=AUTH_TOKEN_FILE,
        full_filepath=full_filepath,
        full_urlpath=full_urlpath
    )
    upload_prc = subprocess.run([upload_cmd], shell=True, stdout=subprocess.PIPE)
    upload_out = upload_prc.stdout.decode('utf-8')

    print(upload_out)

    return 0

def help_message():
    print("USAGE: {} <TARGET_REPO> <LOCAL_FILEPATH> <NEXUS_FILEPATH>".format(sys.argv[0]))
    return

if __name__ == "__main__":
    mandatory_arguments = []
    try:
        (mandatory_arguments, _) = standard_utils.get_arguments( sys.argv, 3 )
    except ValueError:
        help_message()
        exit(1)
    [_, TARGET_REPO, local_filepath, nexus_filepath] = mandatory_arguments

    CLIENT_CONFIG = standard_utils.initialize_configs_from_file( CLIENT_CONFIG_FILE ) 
    
    exit_code = upload_file_to_mvn(local_filepath, nexus_filepath)
    # print("exit {}".format(exit_code))
    exit(exit_code)
