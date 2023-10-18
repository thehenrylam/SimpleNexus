#!/bin/python3

import yaml
import os

# Attempt to get the arguments 
def get_arguments(arguments, minimum_expected_arguments = 0, maximum_expected_arguments = 0):
    # If the list of arguments is less than the number of expected arguments, then exit
    if len(arguments) <= minimum_expected_arguments:
        raise ValueError("list of arguments does not meet minimum_expected arguments: {}".format(minimum_expected_arguments))
        # return
        # help_message()
        # exit(1)
    # If the list of arguments has an empty string, then exit
    number_of_empty_arguments = len( [arguments[i] for i in range(minimum_expected_arguments + 1) if len(arguments[i]) == 0] )
    if (number_of_empty_arguments > 0):
        raise ValueError("list of arguments that are mandatory (length: {}) is empty.".format(minimum_expected_arguments))
        # return
        # help_message()
        # exit(1)
    # Split the arguments into mandatory_arguments and optional_arguments
    [mandatory_arguments, optional_arguments] = [
        arguments[:minimum_expected_arguments + 1], 
        arguments[minimum_expected_arguments + 1 : maximum_expected_arguments + 1]
    ]
    # Padd out the optional arguments (if the maximum_expected arguments is higher than the entire list of arguments)
    optional_arguments = optional_arguments + ["" for i in range(max(maximum_expected_arguments + 1 - len(arguments), 0))]
    return [mandatory_arguments, optional_arguments]

# Initialize the client config
def initialize_configs_from_file(config_filepath):
    output = dict()
    with open(config_filepath, "r") as stream:
        try:
            output = yaml.safe_load(stream)
        except:
            raise exc
    return output
