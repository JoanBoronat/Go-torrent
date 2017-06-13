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

    # Join the group
    def join(self, group_hash):
        if group_hash not in self.swarms:
            self.swarms[group_hash] = {}

    # Leave the group
    def leave(self, group_hash, peer_ref):
        del self.swarms[group_hash][peer_ref]

    # Announce a peer (keep alive)
    def announce(self, group_hash, peer_ref):
        self.swarms[group_hash][peer_ref] = 10

    # Update the counters of the peers deleting the ones
    # that haven't been announced for the last 10 sec
    def update_peers(self):
        self.cycle += 1
        for swarm in self.swarms:
            for peers in self.swarms[swarm].keys():
                self.swarms[swarm][peers] -= 1
                if self.swarms[swarm][peers] == 0:
                    del self.swarms[swarm][peers]

    # Send the list of neighbors to a peer
    def get_members(self, group_hash, sender):
        # Send the list if everyone has joined the group
        if self.num_peers == len(self.swarms[group_hash]):
            tmp = self.swarms[group_hash].keys()
            # Send only the neighbours
            if sender in tmp:
                tmp.remove(sender)
            sender.receive_peers(tmp)
