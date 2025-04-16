#!/bin/bash
KERNEL_VER=$(uname -r)
# random job id
JOB_ID=$(openssl rand -hex 12)
IMG=$1
if [ -z "$1" ]; then
    IMG=base_ebpf:latest
fi
if [ ! -d /var/log/abra ]; then
    mkdir /var/log/abra
fi
if [ ! -d /var/log/abra/$JOB_ID ]; then
    mkdir /var/log/abra/$JOB_ID
fi
podman run --name $JOB_ID --privileged --tmpfs /run --tmpfs /run/lock -v /sys/fs/cgroup:/sys/fs/cgroup:rw -v /usr/src/kernels/$KERNEL_VER:/usr/src/kernels/$KERNEL_VER:ro -v /lib/modules/$KERNEL_VER:/lib/modules/$KERNEL_VER:ro -v /var/log/abra/$JOB_ID:/var/log/ebpf:rw -p 5801:5801 -p 7681:7681 --cap-add audit_write,audit_control -d $IMG