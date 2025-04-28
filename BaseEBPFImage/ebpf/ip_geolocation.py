#!/usr/bin/env python3
from bcc import BPF
import socket
import struct
import geoip2.database
import time
import signal

bpf_text = r"""
#include <uapi/linux/ptrace.h>
#include <net/sock.h>
#include <bcc/proto.h>

int trace_connect(struct pt_regs *ctx, struct sock *sk) {
    u8 family = sk->__sk_common.skc_family;
    if (family != AF_INET) {
        return 0;
    }
    u32 daddr = sk->__sk_common.skc_daddr;
    bpf_trace_printk("%x\n", daddr);
    return 0;
}
"""

b = BPF(text=bpf_text)
b.attach_kprobe(event="tcp_v4_connect", fn_name="trace_connect")

GEOIP_DB = "/usr/local/share/GeoLite2-City.mmdb"
reader = geoip2.database.Reader(GEOIP_DB)

def handle_sigterm(signum, frame):
  print("Termination signal received. Cleaning up...")
  exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGKILL, handle_sigterm)

print("Tracing outgoing IPv4 connections... Ctrl-C to exit.")
# read from the BPF trace buffer
# open new file as append mode, raw bytes
with open("/var/log/ebpf/ip_geolocation.log","a+") as f:
  while True:
    try:
      # b.trace_print() yields lines like: "FFFFFFF [timestamp] 0100007F"
      (task, pid, cpu, flags, ts, msg) = b.trace_fields(nonblocking=False)
      hex_ip = msg.strip()
      ip_int = int(hex_ip, 16)
      # convert to dotted quad
      ip_str = socket.inet_ntoa(struct.pack(">I", ip_int))
      # geolocate
      try:
        geo = reader.city(ip_str)
        country = geo.country.name or "N/A"
        city = geo.city.name or "N/A"
        loc = f"{city}, {country}"
      except Exception:
        loc = "Unknown"
      f.write(f"{time.strftime('%H:%M:%S')} -> {ip_str} ({loc})")
    except KeyboardInterrupt:
      print("\nDetaching, bye!")
      break
