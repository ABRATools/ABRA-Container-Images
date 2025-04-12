KERNEL_VER=$(uname -r)
JOB_ID=3
podman run --name $JOB_ID --privileged --tmpfs /run --tmpfs /run/lock -v /sys/fs/cgroup:/sys/fs/cgroup:rw -v /usr/src/kernels/$KERNEL_VER:/usr/src/kernels/$KERNEL_VER:ro -v /lib/modules/$KERNEL_VER:/lib/modules/$KERNEL_VER:ro -v /var/log/abra/$JOB_ID:/var/log/ebpf:rw --cap-add audit_write,audit_control -d podman-debian
#podman run --name $JOB_ID --privileged --tmpfs /run --tmpfs /run/lock -v /sys/fs/cgroup:/sys/fs/cgroup:rw -v /usr/src/kernels/$KERNEL_VER:/usr/src/kernels/$KERNEL_VER:ro -v /lib/modules/$KERNEL_VER:/lib/modules/$KERNEL_VER:ro -v /var/log/abra/$JOB_ID:/var/log:rw -p 5801:5801 -p 7681:7681 --cap-add audit_write,audit_control -d podman-debian
