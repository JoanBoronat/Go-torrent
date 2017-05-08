from __future__ import division
from pyactor.context import interval
import random


class Group(object):
    _tell = ['announce', 'update_peers', 'init_group', 'get_members', 'join']
    _ref = ['join', 'announce', 'get_members']

    def __init__(self):
        self.swarms = {}
        self.interval = ''
        self.cycle = 0

    def init_group(self):
        self.interval = interval(self.host, 1, self.proxy, "update_peers")

    def join(self, torrent_hash, peer_ref):
        if torrent_hash not in self.swarms:
            self.swarms[torrent_hash] = {}
        # Initialize de counter of the peer at 10 sec.
        self.announce(torrent_hash, peer_ref)

    def leave(self, torrent_hash, peer_ref):
        del self.swarms[torrent_hash][peer_ref]

    # Announce a peer in a swarm
    def announce(self, torrent_hash, peer_ref):
        self.swarms[torrent_hash][peer_ref] = 10

    # Update the counters of the peers deleting the ones
    # that haven't been announced the last 10 sec
    def update_peers(self):
        self.cycle += 1
        for swarm in self.swarms:
            for peers in self.swarms[swarm].keys():
                self.swarms[swarm][peers] -= 1
                if self.swarms[swarm][peers] == 0:
                    del self.swarms[swarm][peers]

    # Send a list of neighbors to a peer
    def get_members(self, torrent_hash, sender):
        tmp = self.swarms[torrent_hash].keys()
        if sender in tmp:
            tmp.remove(sender)

        if len(tmp) >= 3:
            sender.receive_peers(random.sample(tmp, 3))
        else:
            sender.receive_peers(tmp)
