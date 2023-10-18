#!/bin/bash

# NOTE: ./<directory>/upload.sh must be executed on the NexusClientScript/ folder

python3 ./scripts/upload_mvn.py mvn "$1" "$2" "$3" "$4" 
exit $? 
