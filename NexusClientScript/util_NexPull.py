#!/bin/python3

import os
import sys
import subprocess
import time

DOWNLOAD_ARTIFACT_SCRIPT_RAW="./download_from_nexus_RAW.sh"
DOWNLOAD_ARTIFACT_SCRIPT_MVN="./download_from_nexus_MVN.sh"

def usage():
    filename=sys.argv[0]
    message = [
            "=== NexPull ===",
            "What it is:",
            "\tHelps quickly and easily pull artifact from a Nexus repo",
            "\tover to a target directory (where the pull_file.txt is)",
            "Usage:",
            "\t{} /path/to/target/destination/pull_file.txt".format(filename),
            "",
            "Example content of pull_file.txt:",
            "```",
            "nexus_repo_01,/path/to/artifact/v1/artifact-v1.jar",
            "nexus_repo_02,/path/to/another-artifact/v3/another-artifact-v3.dll",
            "...",
            "nexus_repo_01,/path/to/yet-another-artifact/v9/yet-another-artifact-v9.bin",
            "```"
    ]
    print("\n".join(message))
    return

def validate_filepath(filepath):
    if (filepath == "--help" or filepath == "-h"):
        usage()
        exit(1)
    if not os.path.exists(filepath):
        print("ERROR: filepath \"{}\" is not valid!".format(filepath))
        exit(1)
    if not os.path.isfile(filepath):
        print("ERROR: filepath \"{}\" does not point to a file!".format(filepath))
        exit(1)
    return

def select_script_by_repo(repo_name):
    output = DOWNLOAD_ARTIFACT_SCRIPT_MVN
    
    if ("raw" in repo_name):
        output = DOWNLOAD_ARTIFACT_SCRIPT_RAW
    elif ("maven" in repo_name):
        output = DOWNLOAD_ARTIFACT_SCRIPT_MVN
    else:
        output = DOWNLOAD_ARTIFACT_SCRIPT_MVN

    return output

def main(filepath):
    dirpath = os.path.dirname(os.path.abspath(filepath)) 
    
    line_count = 0

    with open(filepath) as fp:
        lines = fp.readlines()
        for l in lines:
            line_count += 1

            # Convert the line to a format that is easier to get useful data from
            l = l.strip()
            l_token = l.split(',')

            # Determine if the formatted data is valid
            if (l == ''):
                # Skip this empty line
                continue
            elif (len(l_token)!=2):
                # If we get an irregular number of tokens, then something is wrong
                print("WARN: Line {} - Non-valid line detected: '{}'".format(line_count, l))
                continue

            # Parse the data into variables that we can use in our operation
            repo_name = l_token[0]
            artifact_path = l_token[1]
            artifact_name = os.path.basename(artifact_path)
            target_path = "{}/{}".format(dirpath,artifact_name)

            download_script = select_script_by_repo(repo_name)
            shell_command = [download_script, artifact_path, target_path]
            print( "Executing: " + " ".join(shell_command) )

            return_code = subprocess.run([DOWNLOAD_ARTIFACT_SCRIPT_MVN, artifact_path, target_path])

            print()

            pass

    return

if __name__ == "__main__":
    num_of_arguments = len(sys.argv)
    if (num_of_arguments != 2):
        usage()
        exit(1)

    filepath=sys.argv[1]
    validate_filepath(filepath)

    main(filepath)

