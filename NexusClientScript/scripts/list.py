#!/bin/python3

import sys
import os
import re
import subprocess

import standard_utils

CLIENT_CONFIG_FILE="./client_config.yml" 
CLIENT_CONFIG=dict()
TARGET_REPO=None

# Execute a curl command to get a list of contents from nexus in the specified repository
def get_html_output(nexus_filepath=""):
    NEXUS_URL = CLIENT_CONFIG["nexus_url"]
    REPO_NAME = CLIENT_CONFIG["repo_name"][ TARGET_REPO ]
    AUTH_TOKEN_FILE = CLIENT_CONFIG["auth_token_file"]
    
    curl_cmd = "curl -u $(cat {auth_token_file}) -X 'GET' {nexus_url}/service/rest/repository/browse/{repo_name}/{nexus_filepath} 2> /dev/null" \
                .format(auth_token_file=AUTH_TOKEN_FILE, nexus_url=NEXUS_URL, repo_name=REPO_NAME, nexus_filepath=nexus_filepath)
    curl_prc = subprocess.run([curl_cmd], shell=True, stdout=subprocess.PIPE)
    output = curl_prc.stdout.decode('utf-8')

    return output

# Convert the html_data (string type) into a tokenized list (list type) 
# and trims it down to a more managable subset of information (In the <table>...</table> section)
def process_html_output(html_data):
    # Convert the html_data into tokens separated by "<" characters
    html_token = [ "<" + t.strip() if len(t.strip()) > 0 else t.strip() for t in html_data.split("<")]

    # Determine the indices where <table... and </table... exists
    table_indices = [-1,-1]
    for i in range(len(html_token)):
        # print(">{}\t {}".format(i, html_token[i]))
        if ("<table" in html_token[i]):
            table_indices[0] = i
        elif ("</table" in html_token[i]):
            table_indices[1] = i

    # print("table_indices: {}".format(table_indices))

    output = html_token[table_indices[0]:table_indices[1]+1]

    # print("\n".join(output))
    
    return output

# Receive relevant links from the list of html_tokens
def get_relevant_links(html_token):
    # Get the subset of the html_token 
    # Get everything with "a href=\"" (EXCEPT for "a href=\"../")
    subset = [ t for t in html_token if "a href=\"" in t and not "a href=\"../" in t ]

    # For each "a href=\"" tag, attempt to extract the URL
    output = []
    for t in subset:
        rgx = re.findall("<a href=\"(.*)\">.*", t)
        if len(rgx) == 0:
            continue
        output.append(rgx[0])

    return output

# Main function
def generate_list_of_nexus_objects(filepath=""):
    NEXUS_URL = CLIENT_CONFIG["nexus_url"]

    # Attempt to clean and validate the output:
    # If the filepath does not have a '/' at the end, attempt to add it
    if (len(filepath) != 0):
        slash = "/" if filepath[-1] != '/' else ""
        filepath = filepath + slash    

    # Attempt to get HTML list of links
    html_output = get_html_output(filepath)
    html_token = process_html_output(html_output)
    list_of_links = get_relevant_links(html_token)

    output = []
    # For each link:
    # If the link is not a full URL, then go deeper into it
    # If the link is a full URL, then print out the output
    for link in list_of_links:
        if (NEXUS_URL not in link):
            new_filepath = filepath + link
            sub_output = generate_list_of_nexus_objects(new_filepath)
            output += sub_output
        else:
            output.append(link)
            pass

    return output

# This method is to help allow other scripts to use the 
# functionality of list.py without needing to rewrite the funtionality from scratch
def api_list_nexus_objects(client_config, target_repo, filepath):
    global CLIENT_CONFIG, TARGET_REPO
    CLIENT_CONFIG = client_config
    TARGET_REPO = target_repo
    return generate_list_of_nexus_objects(filepath)

def help_message():
    print("USAGE: {} <TARGET_REPO> [Optional: NEXUS_FILEPATH]".format(sys.argv[0]))
    return

if __name__ == "__main__":
    mandatory_arguments, optional_arguments = [], []
    try:
        (mandatory_arguments, optional_arguments) = standard_utils.get_arguments( sys.argv, 1, 2 )
    except ValueError:
        help_message()
        exit(1)
    [_, TARGET_REPO] = mandatory_arguments
    [nexus_filepath] = optional_arguments

    CLIENT_CONFIG = standard_utils.initialize_configs_from_file( CLIENT_CONFIG_FILE ) 

    output = generate_list_of_nexus_objects(nexus_filepath)
    # Output the result for shell scripts to capture its output
    [ print(x) for x in output ]

