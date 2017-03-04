import unittest
from pyactor.context import set_context, create_host, sleep, shutdown
from src.tracker import *
from src.peer import *


class PeerTest(unittest.TestCase):
    def test_tracker(self):

        try:
            set_context()
        except:
            pass

        h = create_host()

        tracker = h.spawn('tracker', Tracker)
        tracker.init_tracker()

        p1 = h.spawn('peer1', Peer)
        p1.init_peer("hash1")

        p2 = h.spawn('peer2', Peer)
        p2.init_peer("hash1")

        p3 = h.spawn('peer3', Peer)
        p3.init_peer("hash1")

        p4 = h.spawn('peer4', Peer)
        p4.init_peer("hash1")

        p5 = h.spawn('peer5', Peer)
        p5.init_peer("hash1")

        p6 = h.spawn('peer6', Peer)
        p6.init_peer("hash1")

        p7 = h.spawn('peer7', Peer)
        p7.init_peer("hash1")

        sleep(3)
        p1.get_peers()

        shutdown()


if __name__ == '__main__':
    unittest.main()
