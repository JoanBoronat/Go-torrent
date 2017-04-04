from pyactor.context import set_context, create_host, sleep, serve_forever
from src.tracker import Tracker
from src.peer import Peer
from src.assistant import Assistant

if __name__ == '__main__':

    number_peers = 100
    number_chunks = 9

    # Protocol used (push, pull, push-pull)
    protocol = "pull"

    set_context()
    h = create_host()
    tracker = h.spawn('tracker', Tracker)
    tracker.init_tracker()
    print "Tracker initialized"

    peers = list()
    sleep(2)

    assistant = h.spawn('assistant', Assistant)
    assistant.init_assistant(number_peers, number_chunks, protocol)
    print "Assistant initialized"

    # Spawn peers
    print "Initializing peers..."
    for i in range(number_peers):
        sleep(0.1)
        peers.append(h.spawn('peer' + str(i), Peer))
        # Initialize peer
        peers[i].init_peer("hash1", number_chunks, protocol)
    print "Peers initialized"

    sleep(2)
    print "Initializing gossip protocol"
    # Make peer0 seed
    assistant.load_file(peers[0])

    serve_forever()
