from pyactor.context import (set_context, create_host, sleep, serve_forever)
import random

# todo: Tracker should work like Registry on Sample 4 of Remote tutorial. Achive to announce the peers to the tracker on different processes.
# todo: Separate traker and peer on different files.
class Tracker(object):
    _tell = ['announce', 'update_peers', 'printa', 'init_tracker']
    _ask = ['get_peers']

    def __init__(self):
        self.swarms = {}
        self.interval = ''

    def init_tracker(self):
        self.interval = self.host.interval(1, self.proxy, "update_peers")

    def announce(self, torrent_hash, peer_ref):
        print 'A peer with hash: ', torrent_hash, ' has been announced'
        if torrent_hash in self.swarms:
            self.swarms[torrent_hash].append({'peer_ref': peer_ref, 'timer': 10})
        else:
            self.swarms[torrent_hash] = ([{'peer_ref': peer_ref, 'timer': 10}])

    def update_peers(self):
        for swarm in self.swarms:
            for peers in self.swarms[swarm]:
                peers['timer'] -= 1
            self.swarms[swarm][:] = [x for x in self.swarms[swarm] if x['timer'] > 0]

    # todo: Make get_peers not return the requesting client reference
    def get_peers(self, torrent_hash):
        if len(self.swarms[torrent_hash]) >= 6:
            return random.sample(self.swarms[torrent_hash], 6)
        else:
            return self.swarms[torrent_hash]

    def printa(self):
        print self.swarms


class Peer(object):
    _tell = ['init_peer', 'get_peers', 'announce_me']
    _ask = []

    def __init__(self):
        self.torrent_hash = {}
        self.tracker = ""
        self.interval = ''

    def init_peer(self, torrent_hash):
        self.tracker = self.host.lookup('tracker')
        self.torrent_hash = torrent_hash
        self.interval = self.host.interval(10, self.proxy, "announce_me")

    def announce_me(self):
        self.tracker.announce(self.torrent_hash, self.proxy)

    def get_peers(self):
        print self.tracker.get_peers(self.torrent_hash)


if __name__ == "__main__":
    set_context()
    h = create_host()
    tracker = h.spawn('tracker', Tracker)
    tracker.init_tracker()

    p1 = h.spawn('peer1', Peer)
    p1.init_peer("hash1")

    p2 = h.spawn('peer2', Peer)
    p2.init_peer("hash2")

    p3 = h.spawn('peer3', Peer)
    p3.init_peer("hash1")

    sleep(5)
    p1.get_peers()

    serve_forever()
