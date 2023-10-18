#!/bin/python3

import sys
import os
import subprocess

import standard_utils
from shell_utils import Shell

CLIENT_CONFIG_FILE="./client_config.yml" 
CLIENT_CONFIG=dict()
TARGET_REPO=None

def download_from_nexus(local_filepath, nexus_filepath):
    NEXUS_URL = CLIENT_CONFIG["nexus_url"]
    REPO_NAME = CLIENT_CONFIG["repo_name"][ TARGET_REPO ]
    AUTH_TOKEN_FILE = CLIENT_CONFIG["auth_token_file"]

    full_filepath = Shell.readlink(local_filepath)
    
    full_urlpath = "{nexus_url}/repository/{repo_name}/{nexus_filepath}".format(nexus_url=NEXUS_URL, repo_name=REPO_NAME, nexus_filepath=nexus_filepath)

    print("OPERATION SUMMARY")
    print("PULL : {full_filepath} <- {full_urlpath}".format(full_filepath=full_filepath, full_urlpath=full_urlpath))

    download_cmd_list = [
        "wget --no-verbose ",
        "--user=$(grep -Go '^[^:]*' {}) ".format(AUTH_TOKEN_FILE),
        "--password=$(grep -Go '[^:]*$' {}) ".format(AUTH_TOKEN_FILE),
        "\"{full_urlpath}\" -O {full_filepath}".format(full_urlpath=full_urlpath, full_filepath=full_filepath)
    ]
    download_cmd = " ".join(download_cmd_list)
    download_prc = subprocess.run([download_cmd], shell=True, stdout=subprocess.PIPE)
    output = download_prc.stdout.decode('utf-8')

    print(output)

    return

# This method is to help allow other scripts to use the
# functinoality of download.py without needing to rewrite the functionality from scratch
def api_download_from_nexus(client_config, target_repo, local_filepath, nexus_filepath):
    global CLIENT_CONFIG, TARGET_REPO
    CLIENT_CONFIG = client_config
    TARGET_REPO = target_repo
    return download_from_nexus(local_filepath, nexus_filepath)

def help_message():
    print("USAGE: {} <TARGET_REPO> <TARGET_FILEPATH> <NEXUS_FILEPATH>".format(sys.argv[0]))
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

    output = download_from_nexus(local_filepath, nexus_filepath)
