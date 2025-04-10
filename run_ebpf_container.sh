#!/bin/bash
podman run --name debian-vnc --tmpfs /run --tmpfs /run/lock -v /sys/fs/cgroup:/sys/fs/cgroup:rw -p 5801:5801 -p 7681:7681 --cap-add=CAP_SYS_ADMIN -d podman-ebpf-debian
