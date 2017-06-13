from pyactor.context import set_context, create_host, sleep, serve_forever, Host


if __name__ == '__main__':

    # Configuration
    number_peers = 5
    url_main = 'http://127.0.0.1:1275/'
    urls = ['http://127.0.0.1:1276/', 'http://127.0.0.1:1277/']

    set_context()
    h = create_host(url_main)

    hosts_peers = map(lambda x: h.lookup_url(x, Host), urls)

    group = h.spawn('group', 'group/Group')
    group.init_group(number_peers)

    monitor = h.spawn('monitor', 'monitor/Monitor')
    monitor.init_monitor()

    peers = list()
    sleep(2)

    # Spawn peers
    for i in range(number_peers):
        sleep(0.1)
        peers.append(hosts_peers[i % len(hosts_peers)].spawn('peer' + str(i), 'peerLamport/Peer'))
        # Initialize peer
        peers[i].init_peer('peer' + str(i), url_main, "hash1")
        peers[i].join()

    sleep(10)
    peers[0].sleep(20)

    serve_forever()
