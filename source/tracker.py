import random
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