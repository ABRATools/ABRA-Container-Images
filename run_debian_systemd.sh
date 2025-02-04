#!/bin/bash
docker run --name debian-vnc --privileged --tmpfs /run --tmpfs /run/lock -v /sys/fs/cgroup:/sys/fs/cgroup:rw -p 5801:5801 -p 7681:7681 -d debian-abra