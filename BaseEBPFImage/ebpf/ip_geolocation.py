#!/usr/bin/env python3
from bcc import BPF
import socket
import struct
import geoip2.database
import time
import signal
import sys

bpf_text = r"""
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
#include <net/sock.h>
#include <bcc/proto.h>

struct data_t {
    u32 pid;
    u32 daddr;
    u16 dport;
    u64 ts_ns;
    char comm[TASK_COMM_LEN];
};

BPF_PERF_OUTPUT(events);

int trace_connect(struct pt_regs *ctx, struct sock *sk) {
    u16 family = sk->__sk_common.skc_family;
    if (family != AF_INET)
        return 0;

    struct data_t data = {};
    data.pid   = bpf_get_current_pid_tgid() >> 32;
    data.ts_ns = bpf_ktime_get_ns();
    data.daddr = sk->__sk_common.skc_daddr;
    data.dport = bpf_ntohs(sk->__sk_common.skc_dport);
    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    events.perf_submit(ctx, &data, sizeof(data));
    return 0;
}
"""

b = BPF(text=bpf_text)
b.attach_kprobe(event="tcp_v4_connect", fn_name="trace_connect")

GEOIP_DB = "/usr/local/share/GeoLite2-City.mmdb"
reader = geoip2.database.Reader(GEOIP_DB)

def sig_exit(signum, frame):
  print("\nDetaching...")
  sys.exit(0)

signal.signal(signal.SIGINT, sig_exit)
signal.signal(signal.SIGTERM, sig_exit)

print("Timestamp,PID,COMM,IP:PORT,(Location)")

# event callback
def print_event(cpu, data, size):
  event = b["events"].event(data)
  with open("/var/log/ebpf/usercommand.log","a+b") as f:
    ip_str = socket.inet_ntoa(struct.pack("<I", event.daddr))
    ts_s = event.ts_ns / 1e9
    ts = time.strftime("%H:%M:%S", time.localtime(ts_s))
    loc = ""
    try:
      geo = reader.city(ip_str)
      country = geo.country.name or "N/A"
      city = geo.city.name or "N/A"
      loc = f"{city}, {country}"
    except Exception:
      loc = "Unknown"
    f.write(f"{ts},{event.pid:<6},{event.comm.decode()},{ip_str}:{event.dport},({loc})\n")

b["events"].open_perf_buffer(print_event)
while True:
  try:
    b.perf_buffer_poll()
  except KeyboardInterrupt:
    sys.exit(0)
  except Exception as e:
    print("Error: %s" % e)
    sys.exit(1)