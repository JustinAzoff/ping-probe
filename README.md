    Usage: ./ping_probe.py count timeout host [host] [host]


    $ ./ping_probe.py  5 1 svn tftp nfs
    2012-08-02 09:08:23 check=PING addr=tftp ok=True sent=5 received=5 packet_loss=0 min_rtt=1.03 avg_rtt=1.09 max_rtt=1.18
    2012-08-02 09:08:23 check=PING addr=svn ok=True sent=5 received=5 packet_loss=0 min_rtt=0.98 avg_rtt=1.17 max_rtt=1.39
    2012-08-02 09:08:23 check=PING addr=nfs ok=True sent=5 received=5 packet_loss=0 min_rtt=1.01 avg_rtt=1.36 max_rtt=2.68


it actually uses a tcp ping to avoid requiring root.
