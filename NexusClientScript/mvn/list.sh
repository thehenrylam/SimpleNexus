#!/bin/bash

# NOTE: ./<directory>/list.sh must be executed on the NexusClientScript/ folder

python3 ./scripts/list.py mvn "$1"
exit $?
