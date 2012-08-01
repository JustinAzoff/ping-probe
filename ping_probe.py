#!/usr/bin/env python
from subprocess import Popen, PIPE
import datetime

import time
import re
import sys

class PingError(Exception):
    pass

def ping(address, count):
    output, err = Popen(["ping", "-q", "-c", str(count), address], stdout=PIPE, stderr=PIPE).communicate()
    try :
        return parse_ping(output)
    except:
        raise PingError(err)

def maybe_int(s):
    if '.' in s:
        func = float
    else:
        func = int

    try:
        return func(s)
    except ValueError:
        return s


def parse_ping(txt):
    lines = txt.strip().split("\n")
    transmitted_line = [x for x in lines if 'transmitted' in x][0]
    stats_line = [x for x in lines if 'min/avg' in x][0]

    #5 packets transmitted, 5 received, 0% packet loss, time 4006ms
    stats = re.match("(?P<sent>\d+) packets transmitted, (?P<received>\d+) received, (?P<loss>\d+)% packet loss,", transmitted_line).groupdict()

    #rtt min/avg/max/mdev = 9.363/11.902/15.020/2.061 ms, pipe 2
    parts = re.split("[ /]", stats_line.split(" = ")[1])
    stats['min'] = parts[0]
    stats['avg'] = parts[1]
    stats['max'] = parts[2]
    stats['mdev'] = parts[3]


    for k,v in stats.items():
        stats[k] = maybe_int(v)

    stats['ok'] = stats['loss'] < 4

    return stats

def format_result(res):
    fmt = "check=PING ok=%(ok)s sent=%(sent)d received=%(received)d packet_loss=%(loss)d min_rtt=%(min).2f avg_rtt=%(avg).2f max_rtt=%(max).2f"
    return fmt % res

if __name__ == "__main__":
    host = sys.argv[1]
    count = int(sys.argv[2])
    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    res = ping(host, count)
    print format_result(res)
