#!/bin/bash

network_name="podman_net"
subnet="192.168.200.0/24"

# Check if the network exists, create it if it doesn't
if podman network inspect $network_name &>/dev/null; then
  echo "Network '$network_name' does already exists. exiting..."
  exit
fi

podman network create --subnet=$subnet $network_name
