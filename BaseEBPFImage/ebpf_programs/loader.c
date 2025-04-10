// loader.c
#include <stdio.h>
#include <bpf/libbpf.h>

int main() {
    struct bpf_object *obj;
    int prog_fd;

    // Open the eBPF object file
    obj = bpf_object__open_file("hello_bpf.o", NULL);
    if (!obj) {
        fprintf(stderr, "ERROR: opening BPF object file\n");
        return 1;
    }

    // Load the eBPF program
    if (bpf_object__load(obj)) {
        fprintf(stderr, "ERROR: loading BPF object file\n");
        return 1;
    }

    // Find and attach the program
    struct bpf_program *prog = bpf_object__find_program_by_title(obj, "kprobe/sys_clone");
    if (!prog) {
        fprintf(stderr, "ERROR: finding a prog in obj\n");
        return 1;
    }

    prog_fd = bpf_program__fd(prog);
    // Attach the program (this uses bpf_attach_kprobe under the hood)
    if (bpf_attach_kprobe(prog_fd, false, "sys_clone", "hello") < 0) {
        fprintf(stderr, "ERROR: attaching kprobe\n");
        return 1;
    }

    printf("eBPF program successfully loaded and attached.\n");
    // Keep the program running to collect events.
    while (1) sleep(1);
    return 0;
}
