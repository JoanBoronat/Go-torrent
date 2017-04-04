from __future__ import division
from pyactor.context import interval
import random


class Tracker(object):
    _tell = ['announce', 'update_peers', 'init_tracker', 'get_peers']
    _ref = ['announce', 'get_peers']

    def __init__(self):
        self.swarms = {}
        self.interval = ''
        self.cycle = 0

    def init_tracker(self):
        self.interval = interval(self.host, 1, self.proxy, "update_peers")

    def announce(self, torrent_hash, peer_ref):
        if torrent_hash not in self.swarms:
            self.swarms[torrent_hash] = {}
        self.swarms[torrent_hash][peer_ref] = 10

    def update_peers(self):
        self.cycle += 1
        for swarm in self.swarms:
            for peers in self.swarms[swarm].keys():
                self.swarms[swarm][peers] -= 1
                if self.swarms[swarm][peers] == 0:
                    del self.swarms[swarm][peers]

    def get_peers(self, torrent_hash, sender):
        tmp = self.swarms[torrent_hash].keys()
        if sender in tmp:
            tmp.remove(sender)
        if len(tmp) >= 3:
            sender.receive_peers(random.sample(tmp, 3))
        else:
            sender.receive_peers(tmp)
