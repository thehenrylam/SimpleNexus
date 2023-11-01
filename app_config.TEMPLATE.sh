#!/bin/bash

DOCKER_IMAGE="sonatype/nexus3" # official x86 support
# DOCKER_IMAGE="klo2k/nexus3" # unofficial ARM support

KEYWORD="Nexus"
IMAGE_NAME="nexus_image"
CONTAINER_NAME="nexus"
VOLUME_NAME="${CONTAINER_NAME}_data"
