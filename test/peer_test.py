import unittest
from pyactor.context import set_context, create_host, sleep, shutdown
from src.tracker import *
from src.peer import *
from src.assistant import *


class PeerTest(unittest.TestCase):

    def test_peer(self):

        try:
            set_context()
        except:
            pass

        number_peers = 5
        number_chunks = 9
        protocol = "push-pull"

        h = create_host()
        tracker = h.spawn('tracker', Tracker)
        tracker.init_tracker()

        peers = list()
        sleep(2)

        assistant = h.spawn('assistant', Assistant)
        assistant.init_assistant(number_peers, number_chunks, protocol)

        for i in range(number_peers):
            peers.append(h.spawn('peer' + str(i), Peer))
            peers[i].init_peer("hash1", number_chunks, protocol)

        sleep(2)
        assistant.load_file(peers[0])

        shutdown()

if __name__ == '__main__':
    unittest.main()
