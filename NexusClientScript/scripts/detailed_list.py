#!/bin/python3

import sys
import os
import re
import subprocess
import json

from standard_utils import initialize_configs_from_file, get_arguments

DEFAULT_CLIENT_CONFIG_FILE="./client_config.yml" 

class NexusListHelper:
    def __init__(self, config_filepath, repo_alias):
        self.config_filepath = config_filepath
        self.repo_alias = repo_alias
        self.config = init_config( self.config_filepath, self.repo_alias )
        return

    def list(self, filepath=""):
        return get_nexus_objects(self.config, filepath)

    def filter(self, json_list, filepath):
        return filter_by_filepath(json_list, filepath)


def filter_by_filepath(json_list, filepath):
    # Get the filepath
    rgx = re.compile( filepath )

    # Get the (reversed) list of indices to remove
    indices_to_remove = []
    for i, j in enumerate(json_list):
        result = rgx.match(j["path"])
        if result is None:
            indices_to_remove.append(i)
    indices_to_remove.reverse()

    # Remove the unwanted indices from the json_list
    for i in indices_to_remove:
        json_list.pop(i)

    return json_list

# Use the rest API to get nexus data
def request_nexus_data(config, continuation_token=None):
    # Get facts
    token_file = config["auth_token_file"]
    nexus_url = config["nexus_url"]
    repo_name = config["_target_repo"]

    # Create the continuation_request (Leave it blank if its None)
    continuation_request = "&continuationToken={}".format(continuation_token) if continuation_token is not None else ""
    # Create the curl command 
    curl_cmd = "curl -u $(cat {token_file}) -X 'GET' \"{nexus_url}/service/rest/v1/assets?repository={repo_name}{continuation_request}&path=MCAWS/gold/\" -H 'accept: application/json' 2>/dev/null" \
            .format(token_file=token_file, nexus_url=nexus_url, repo_name=repo_name, continuation_request=continuation_request)
    # Launch the curl command
    curl_prc = subprocess.run([curl_cmd], shell=True, stdout=subprocess.PIPE)

    # Get the output (expected to be json data)
    json_text = curl_prc.stdout.decode('utf-8')
    # Get Json data
    json_data = json.loads( json_text )
    
    return json_data

# Execute a curl command to get a list of contents from nexus in the specified repository
def get_nexus_objects(config, filepath="", continuation_token=None):
    # Attempt to clean and validate the output:
    # If the filepath does not have a '/' at the end, attempt to add it
    #if (len(filepath) != 0):
    #    slash = "/" if filepath[-1] != '/' else ""
    #    filepath = filepath + slash    

    # Request nexus data
    json_data = request_nexus_data( config, continuation_token )

    # Attempt to extract the output, and default to an empty list if its None
    output = json_data["items"] if json_data["items"] is not None else []
    output = filter_by_filepath(output, filepath)

    # If the continuation token is not None, then attempt to get its contents 
    new_continuation_token = json_data["continuationToken"]
    if (new_continuation_token is not None):
        output += get_nexus_objects( config, filepath, new_continuation_token )

    return output

# Initialize the config
def init_config(config_file, repo_alias):
    if not os.path.exists( config_file ):
        raise FileNotFoundError("config file '{}' does not exist!".format(config_file))

    # Get the config from the client_config_file
    config = initialize_configs_from_file( config_file )

    if repo_alias not in config["repo_name"]:
        raise KeyError("Unable to find repo_alias '{}' within config['repo_name'] in config file '{}'".format(repo_alias, config_file))

    # Add a new entry where the full target repo name is injected as temporary data in the config dictionary
    config["_target_repo"] = config["repo_name"][ repo_alias ]
    return config

def help_message():
    print("USAGE: {} <TARGET_REPO_ALIAS> [Optional: NEXUS_FILEPATH]".format(sys.argv[0]))
    return

if __name__ == "__main__":
    mandatory_arguments, optional_arguments = [], []
    try:
        (mandatory_arguments, optional_arguments) = get_arguments( sys.argv, 1, 2 )
    except ValueError:
        help_message()
        exit(1)
    [_, repo_alias] = mandatory_arguments
    [nexus_filepath] = optional_arguments

    # Get nexus objects
    config = init_config( DEFAULT_CLIENT_CONFIG_FILE, repo_alias )
    output = get_nexus_objects(config, nexus_filepath)

    # Output the result for shell scripts to capture its output
    # [ print(json.dumps(x, indent=4)) for x in output ]
    [ print(x["path"]) for x in output ]
    # filter_by_filepath( output, nexus_filepath )

