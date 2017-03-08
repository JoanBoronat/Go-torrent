from pyactor.context import set_context, create_host, sleep, serve_forever
from src.tracker import *
from src.peer import *

if __name__ == '__main__':

    set_context()
    h = create_host()
    tracker = h.spawn('tracker', Tracker)
    tracker.init_tracker()

    peers = list()
    sleep(2)

    # Spawn 5 peers
    for i in range(5):
        peers.append(h.spawn('peer' + str(i), Peer))
        sleep(2)
        # Initialize peer
        peers[i].init_peer("hash1", 9)

    sleep(2)
    # Make peer0 seed
    peers[0].load_file()

    serve_forever()
