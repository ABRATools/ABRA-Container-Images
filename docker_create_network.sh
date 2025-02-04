#!/bin/bash
network_name="docker_net"
if docker network inspect $network_name &>/dev/null; then
  echo "Error: Docker network '$network_name' already exists!"
  exit
fi

docker network create --driver bridge --subnet=192.168.100.0/24 $network_name

