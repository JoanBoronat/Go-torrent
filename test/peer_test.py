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

        peers = list()
        sleep(1)

        # Spawn 5 peers
        for i in range(2):
            peers.append(h.spawn('peer' + str(i), Peer))
            sleep(0.5)
            # Initialize peer
            peers[i].init_peer("hash1", 9)

        # Make peer0 seed
        peers[0].load_file()

        shutdown()

if __name__ == '__main__':
    unittest.main()
