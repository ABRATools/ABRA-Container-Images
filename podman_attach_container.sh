#!/bin/bash

# Variables
image=$1
container_name=$1
network_name="podman_net"

# Validate input
if [[ -z $image || -z $container_name ]]; then
  echo "Must supply Docker image name!"
  exit 1
fi

# Check if the network exists, create it if it doesn't
if ! podman network inspect $network_name &>/dev/null; then
  echo "Network '$network_name' does not exist. exiting..."
  exit
fi

# Run container with automatic IP assignment
podman run -d --name "$container_name" --network "$network_name" "$image"

# Get assigned IP
container_ip=$(podman inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$container_name")

# Display success message
echo "Container '$container_name' started successfully on network '$network_name'"
echo "Assigned IP: $container_ip"
