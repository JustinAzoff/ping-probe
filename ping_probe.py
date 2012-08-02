#!/usr/bin/env python
from subprocess import Popen, PIPE
import datetime

import time
import re
import sys

import errno
import socket

def tcping(host, port=65533, timeout=2):
    s = socket.socket()
    s.settimeout(timeout)
    end = None
    try:
        start = time.time()
        s.connect((host, port))
        s.close()
        end = time.time()
    except Exception, e:
        if e.errno == errno.ECONNREFUSED:
            end = time.time()
    if end:
        ms = 1000*(end-start)
        return round(ms,2)

def ping(host, count, timeout=2):
    res = []
    for _ in range(count):
        r = tcping(host, timeout=timeout)
        if r:
            time.sleep((timeout*1000 - r)/1000.0)
        res.append(r)
    return res

def ping_stats(results):
    stats = {}
    not_none = [r for r in results if r is not None]
    if not not_none:
        stats = dict.fromkeys(("min","max","avg"), None)
        stats["loss"] = 100
    else:
        stats["min"] = min(not_none)
        stats["max"] = max(not_none)
        stats["avg"] = sum(not_none) / len(not_none)

    stats["sent"] = len(results)
    stats["received"] = len(not_none)

    stats["loss"] = 100*(stats["sent"] - stats["received"]) / stats["sent"]
    stats['ok'] = stats['loss'] < 4

    return stats

def format_result(res):
    if res["max"]:
        fmt = "check=PING host=%(host)s ok=%(ok)s sent=%(sent)d received=%(received)d packet_loss=%(loss)d min_rtt=%(min).2f avg_rtt=%(avg).2f max_rtt=%(max).2f"
    else:
        fmt = "check=PING host=%(host)s ok=%(ok)s sent=%(sent)d received=%(received)d packet_loss=%(loss)d min_rtt=nan avg_rtt=nan max_rtt=nan"
    return fmt % res

if __name__ == "__main__":
    host = sys.argv[1]
    count = int(sys.argv[2])
    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    res = ping_stats(ping(host, count))
    res["host"] = host
    print format_result(res)
