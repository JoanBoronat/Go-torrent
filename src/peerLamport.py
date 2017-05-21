from __future__ import division
from pyactor.context import interval, sleep
import random


class Peer(object):
    _tell = ['init_peer', 'announce', 'get_members', 'receive_peers', 'receive', 'multicast', 'join', 'leave', 'sleep',
             'send_data', 'receive_ack', 'process_msg']
    _ref = ['receive_peers', 'init_peer']
    _ask = ['get_sequence']

    def __init__(self):
        self.group_hash = ''
        self.chunks = []
        self.queue = {}
        self.nextSeq = 0
        self.neighbors = []
        self.msgs = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        self.clock = 0

    def init_peer(self, id, url_group, group_hash, null):
        self.id = id
        self.group = self.host.lookup_url(url_group + 'group', 'Group', 'group')
        self.monitor = self.host.lookup_url(url_group + 'monitor', 'Monitor', 'monitor')
        self.group_hash = group_hash
        print self.id + " initialized"

    def join(self):
        self.group.join(self.group_hash, self.proxy)
        # Announce the peer every 10 seconds
        self.interval = interval(self.host, 10, self.proxy, "announce")
        self.interval_members = interval(self.host, 2, self.proxy, "get_members")
        self.interval_multicast = interval(self.host, 2, self.proxy, "multicast")
        self.interval_data = interval(self.host, 1, self.proxy, "send_data")
        self.interval_msg = interval(self.host, 2, self.proxy, "process_msg")

    def leave(self):
        self.group.leave(self.group_hash, self.proxy)

    # Announce myself to the group in a swarm
    def announce(self):
        self.group.announce(self.group_hash, self.proxy)

    # Get neighbors (asynchronous call)
    def get_members(self):
        self.group.get_members(self.group_hash, self.proxy)

    # Receive the requested peers
    def receive_peers(self, neighbors):
        self.neighbors = neighbors
        self.interval_members.set()

    # Receive the data from another peer
    def receive(self, m, ts, processid):
        if (ts, processid) in self.queue:
            self.queue[(ts, processid)]['msg'] = m
        else:
            self.queue[(ts, processid)] = {"ackCounter": 0, "msg": m}
        if ts > self.clock:
            self.clock = ts
        for neighbor in self.neighbors:
            neighbor.receive_ack(ts, processid)
        self.receive_ack(ts, processid)

    # Push the data I have to a random neighbor
    def multicast(self):
        if self.neighbors:
            m = random.choice(self.msgs)
            self.clock += 1
            for neighbor in self.neighbors:
                neighbor.receive(m, self.clock, self.id)
            self.receive(m, self.clock, self.id)

    def receive_ack(self, ts, processid):
        if (ts, processid) in self.queue:
            self.queue[(ts, processid)]["ackCounter"] += 1
        else:
            self.queue[(ts, processid)] = {"ackCounter": 1}

    def process_msg(self):
        if len(self.queue) >= 1:
            keys = self.queue.keys()
            keys.sort()
            if self.queue[keys[0]]["ackCounter"] == len(self.neighbors) + 1:
                self.chunks.append(self.queue[keys[0]]["msg"])
                del self.queue[keys[0]]

    def sleep(self, n):
        print self.id, "I'll be asleep for", n, "seconds"
        sleep(n)
        print self.id, "I just wake up!"

    def send_data(self):
        self.monitor.receive_data(self.id, self.chunks)
