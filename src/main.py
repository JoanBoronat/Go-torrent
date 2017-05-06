from pyactor.context import set_context, create_host, sleep, serve_forever, Host


if __name__ == '__main__':

    # Configuration
    protocol = "push-pull"
    number_peers = 20
    number_chunks = 9
    urls = ['http://127.0.0.1:1277/', 'http://127.0.0.1:1277/', 'http://127.0.0.1:1277/']

    set_context()
    h = create_host('http://127.0.0.1:1277/')

    host_tracker = h.lookup_url(urls[0], Host)
    host_assistant = h.lookup_url(urls[1], Host)
    host_peers = h.lookup_url(urls[2], Host)

    tracker = host_tracker.spawn('tracker', 'tracker/Tracker')
    tracker.init_tracker()
    print 'Tracker initialized'

    peers = list()
    sleep(2)

    assistant = host_assistant.spawn('assistant', 'assistant/Assistant')
    assistant.init_assistant(number_peers, number_chunks, protocol)
    print "Assistant initialized"

    # Spawn peers
    for i in range(number_peers):
        sleep(0.1)
        peers.append(host_peers.spawn('peer' + str(i), 'peer/Peer'))
        # Initialize peer
        peers[i].init_peer(urls[0], urls[1], "hash1", number_chunks, protocol)
    print "Peers initialized"

    sleep(2)
    print "Initializing gossip with " + protocol + " protocol"

    # Make peer0 seed
    assistant.load_file(peers[0])
    assistant.print_data_start()

    serve_forever()
