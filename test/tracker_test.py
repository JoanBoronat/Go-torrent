import unittest
from pyactor.context import set_context, create_host, sleep, shutdown
from src.tracker import *
from src.peer import *
from src.assistant import *


class PeerTest(unittest.TestCase):
    def setUp(self):
        try:
            set_context()
        except:
            pass

        try:
            self.h = create_host()
        except:
            pass

    def test_tracker(self):

        number_peers = 5
        number_chunks = 9

        protocol = "push-pull_data"

        tracker = self.h.spawn('tracker', Tracker)
        tracker.init_tracker()

        self.peers = list()
        sleep(2)

        assistant = self.h.spawn('assistant', Assistant)
        assistant.init_assistant(number_peers, number_chunks, protocol)

        for i in range(number_peers):
            self.peers.append(self.h.spawn('peer' + str(i), Peer))
            self.peers[i].init_peer("hash1", number_chunks, protocol)

        sleep(2)
        self.peers[0].set_data({0: "A", 1: "S", 2: "D", 3: "F"})
        tracker.announce("torrenthash", "peerref")
        sleep(12)

        shutdown()


if __name__ == '__main__':

    unittest.main()
