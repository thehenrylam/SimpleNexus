#!/bin/bash

# NOTE: ./<directory>/remove.sh must be executed on the NexusClientScript/ folder

python3 ./scripts/remove.py raw "$1"
exit $?
