import random


class Tracker(object):
    _tell = ['announce', 'update_peers', 'init_tracker']
    _ask = ['get_peers']
    _ref = ['announce']

    def __init__(self):
        self.swarms = {}
        self.interval = ''

    def init_tracker(self):
        self.interval = self.host.interval(1, self.proxy, "update_peers")

    def announce(self, torrent_hash, peer_ref):
        if torrent_hash not in self.swarms:
            self.swarms[torrent_hash] = {}
        self.swarms[torrent_hash][peer_ref] = 10

    def update_peers(self):
        for swarm in self.swarms:
            for peers in self.swarms[swarm].keys():
                self.swarms[swarm][peers] -= 1
                if self.swarms[swarm][peers] == 0:
                    del self.swarms[swarm][peers]

    def get_peers(self, torrent_hash, sender):
        tmp = self.swarms[torrent_hash].copy()
        if len(tmp) >= 6:
            return random.sample(tmp, 6)
        else:
            return tmp
