from pyactor.context import (set_context, create_host, sleep, serve_forever)
from peer import *
from tracker import *

# todo: Tracker should work like Registry on Sample 4 of Remote tutorial. Achive to announce the peers to the tracker on different processes.

if __name__ == "__main__":
    set_context()
    h = create_host()
    tracker = h.spawn('tracker', Tracker)
    tracker.init_tracker()

    p1 = h.spawn('peer1', Peer)
    p1.init_peer("hash1")

    p2 = h.spawn('peer2', Peer)
    p2.init_peer("hash2")

    p3 = h.spawn('peer3', Peer)
    p3.init_peer("hash1")

    sleep(5)
    p1.get_peers()

    serve_forever()
