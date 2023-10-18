#!/bin/bash

# NOTE: ./<directory>/remove.sh must be executed on the NexusClientScript/ folder

python3 ./scripts/remove.py mvn "$1"
exit $?
