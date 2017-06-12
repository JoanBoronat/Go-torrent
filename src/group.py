from __future__ import division
from pyactor.context import interval


class Group(object):
    _tell = ['announce', 'update_peers', 'init_group', 'get_members', 'join', 'leave']
    _ref = ['join', 'announce', 'get_members']

    def __init__(self):
        self.swarms = {}
        self.interval = ''
        self.cycle = 0
        self.num_peers = None

    def init_group(self, num_peers):
        self.interval = interval(self.host, 1, self.proxy, "update_peers")
        self.num_peers = num_peers
        print 'Group initialized'

    def join(self, group_hash):
        if group_hash not in self.swarms:
            self.swarms[group_hash] = {}

    def leave(self, group_hash, peer_ref):
        del self.swarms[group_hash][peer_ref]

    # Announce a peer in a swarm
    def announce(self, group_hash, peer_ref):
        self.swarms[group_hash][peer_ref] = 10

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
    def get_members(self, group_hash, sender):
        if self.num_peers == len(self.swarms[group_hash]):
            tmp = self.swarms[group_hash].keys()
            if sender in tmp:
                tmp.remove(sender)
            sender.receive_peers(tmp)
