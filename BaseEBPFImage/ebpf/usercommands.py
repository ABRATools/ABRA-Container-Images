#!/usr/bin/python3
#monitor all user commands

from bcc import BPF
from time import sleep
from bcc.utils import printb
import signal

bpf_text="""
#include <linux/sched.h>

struct data_t {
  u32 pid;
  u64 ts;
  char command[32];
  char comm[TASK_COMM_LEN];
};
BPF_PERF_OUTPUT(events);

int printCommands(struct pt_regs *ctx){
  struct data_t data={};

  data.pid=bpf_get_current_pid_tgid();
  data.ts=bpf_ktime_get_ns();
  bpf_probe_read_user_str(&data.command,sizeof(data.command),(void *)PT_REGS_RC(ctx));
  bpf_get_current_comm(&data.comm,sizeof(data.comm));

  //bpf_probe_read_user_str(&command,sizeof(command),(void *)PT_REGS_RC(ctx));
  //bpf_trace_printk("%s",command);
  events.perf_submit(ctx,&data,sizeof(data));
  return 0;
}
"""

#add output to line

b=BPF(text=bpf_text)
b.attach_uretprobe(name="/bin/bash",sym="readline",fn_name="printCommands")

def handle_sigterm(signum, frame):
  print("Termination signal received. Cleaning up...")
  exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGKILL, handle_sigterm)

print("%-6s %-16s %-64s" % ("PID", "COMM", "COMMAND"))

def print_event(cpu,data,size):
  event=b["events"].event(data)
  with open("/var/log/ebpf/usercommand.log","a+b") as f:
    f.write(b"%-12d %-6d %-16s %s\n" % (event.ts,event.pid,event.comm,event.command))

b[b"events"].open_perf_buffer(print_event)
while(1):
  try:
    b.perf_buffer_poll()
  except KeyboardInterrupt:
    #log.close()
    exit()