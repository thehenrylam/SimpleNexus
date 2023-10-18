#!/bin/python3

import sys
import os
import subprocess

import list
import standard_utils

CLIENT_CONFIG_FILE="./client_config.yml" 
CLIENT_CONFIG=dict()
TARGET_REPO=None

def is_directory(filepath):
    if (len(filepath) == 0):
        raise ValueError("ERROR: Invalid filepath due to empty string")
    return filepath[-1] == '/'

def delete_folder(filepath):
    list_of_urlpaths = list.api_list_nexus_objects(CLIENT_CONFIG, TARGET_REPO, nexus_filepath)

    for f in list_of_urlpaths:
        execute_delete( f )

    return

def delete_file(filepath):
    NEXUS_URL = CLIENT_CONFIG["nexus_url"]
    REPO_NAME = CLIENT_CONFIG["repo_name"][ TARGET_REPO ]

    full_urlpath = "{nexus_url}/repository/{repo_name}/{filepath}".format(nexus_url=NEXUS_URL, repo_name=REPO_NAME, filepath=filepath)
    
    execute_delete(full_urlpath)

    return

def execute_delete(full_urlpath):
    AUTH_TOKEN_FILE = CLIENT_CONFIG["auth_token_file"]

    print("REMOVE : {}".format(full_urlpath))
    
    delete_cmd = "curl -u $(cat {auth_token_file}) -X 'DELETE' \"{full_urlpath}\" 2> /dev/null".format(
        auth_token_file=AUTH_TOKEN_FILE, 
        full_urlpath=full_urlpath
    )
    delete_prc = subprocess.run([delete_cmd], shell=True, stdout=subprocess.PIPE)
    delete_out = delete_prc.stdout.decode('utf-8')

    print(delete_out)

    return

def main(filepath):
    if (len(filepath) == 0): 
        print("ERROR: Unable to accept the filepath to be an empty string")
        exit(1)
    
    print("OPERATION SUMMARY")

    is_dir = is_directory(filepath)
    if (is_dir):
        print("Remove directory : '{}'".format(filepath))
        delete_folder(filepath)
        pass
    else:
        print("Remove file : '{}'".format(filepath))
        delete_file(filepath)
        pass

    return

def help_message():
    print("USAGE: {} <TARGET_REPO> <NEXUS_FILEPATH>".format(sys.argv[0]))
    return

if __name__ == "__main__":
    mandatory_arguments = []
    try:
        (mandatory_arguments, _) = standard_utils.get_arguments( sys.argv, 2 )
    except ValueError:
        help_message()
        exit(1)
    [_, TARGET_REPO, nexus_filepath] = mandatory_arguments

    CLIENT_CONFIG = standard_utils.initialize_configs_from_file( CLIENT_CONFIG_FILE )

    output = main(nexus_filepath)
