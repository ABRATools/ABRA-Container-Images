#!/bin/bash

image=$1
container_name=$1
network_name="docker_net"

# Validate input
if [[ -z $image || -z $container_name ]]; then
  echo "Must supply Docker image name!"
  exit 1
fi

# Check if the network exists
if ! docker network inspect $network_name &>/dev/null; then
  echo "Error: Docker network '$network_name' does not exist!"
  exit 1
fi

# Run container with automatic IP assignment
docker run -d --name "$container_name" --net "$network_name" "$image"

# Get assigned IP
container_ip=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$container_name")

# Display success message
echo "Container '$container_name' started successfully on network '$network_name'"
echo "Assigned IP: $container_ip"
