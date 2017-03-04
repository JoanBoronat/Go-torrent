import unittest
from pyactor.context import set_context, create_host, sleep, shutdown
from src.tracker import *
from src.peer import *

class PeerTest(unittest.TestCase):

    def test_peer(self):

        try:
            set_context()
        except:
            pass

        h = create_host()
        tracker = h.spawn('tracker', Tracker)
        tracker.init_tracker()

        p1 = h.spawn('peer1', Peer)
        p1.init_peer("hash1")

        sleep(1)
        p1.get_peers()

        shutdown()

if __name__ == '__main__':
    unittest.main()
