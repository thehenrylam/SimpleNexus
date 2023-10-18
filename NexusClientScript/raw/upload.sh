#!/bin/bash

# NOTE: ./<directory>/upload.sh must be executed on the NexusClientScript/ folder

python3 ./scripts/upload_raw.py raw "$1" "$2" 
exit $? 
