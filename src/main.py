from pyactor.context import set_context, create_host, sleep, serve_forever, Host


if __name__ == '__main__':

    # Configuration
    number_peers = 5
    urls = ['http://127.0.0.1:1277/', 'http://127.0.0.1:1277/', 'http://127.0.0.1:1277/']

    set_context()
    h = create_host(urls[2])

    host_group = h.lookup_url(urls[0], Host)
    host_monitor = h.lookup_url(urls[1], Host)
    host_peers = h.lookup_url(urls[2], Host)

    group = host_group.spawn('group', 'group/Group')
    group.init_group(number_peers)

    monitor = host_monitor.spawn('monitor', 'monitor/Monitor')
    monitor.init_monitor()

    peers = list()
    sleep(2)

    # Spawn peers
    for i in range(number_peers):
        sleep(0.1)
        peers.append(host_peers.spawn('peer' + str(i), 'peer/Peer'))
        # Initialize peer
        peers[i].init_peer('peer' + str(i), urls[0], "hash1", peers[0])
        peers[i].join()

    sleep(7)
    peers[0].sleep(20)

    peers[1].sleep(20)

    sleep(2)

    serve_forever()
