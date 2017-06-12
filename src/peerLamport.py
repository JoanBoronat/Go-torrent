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
        self.group.join(self.group_hash)
        self.interval = interval(self.host, 10, self.proxy, "announce")  # Keep alive
        self.interval_members = interval(self.host, 2, self.proxy, "get_members")
        self.interval_data = interval(self.host, 1, self.proxy, "send_data")  # Monitoring data

    def leave(self):
        self.group.leave(self.group_hash, self.proxy)

    # Announce myself to the group.
    def announce(self):
        self.group.announce(self.group_hash, self.proxy)

    # Get neighbors (asynchronous call)
    def get_members(self):
        self.group.get_members(self.group_hash, self.proxy)

    # Receive the requested neighbors once they are all announced to the group
    def receive_peers(self, neighbors):
        self.neighbors = neighbors
        self.interval_members.set()  # Stop asking for neighbors
        sleep(3)  # Wait to allow peers get their neighbors
        self.interval_multicast = interval(self.host, 1, self.proxy, "multicast")  # Start sending data

    # Receive the data from another peer
    def receive(self, m, ts, processid):
        # Check if the ID is already in queue because someone sent an ACK
        if (ts, processid) in self.queue:
            self.queue[(ts, processid)]['msg'] = m
        else:
            self.queue[(ts, processid)] = {"ackCounter": 0, "msg": m}
        if ts > self.clock:
            self.clock = ts  # Updating clock
        map(lambda x: x.receive_ack(ts, processid), self.neighbors)  # ACK the msg to all my neighbors

    # Push the data I have to a random neighbor
    def multicast(self):
        if self.neighbors:
            m = random.choice(self.msgs)
            self.clock += 1
            map(lambda x: x.receive(m, self.clock, self.id), self.neighbors)  # Sending msg to my neighbors
            self.receive(m, self.clock, self.id)  # Sending msg to myself

    # Receive ACK from neighbors
    def receive_ack(self, ts, processid):
        # Check if the message is in the queue
        if (ts, processid) in self.queue:
            self.queue[(ts, processid)]["ackCounter"] += 1
            # If every neighbor has sent the ACK I can process the msg
            if self.queue[(ts, processid)]["ackCounter"] == len(self.neighbors):
                self.process_msg()
        else:
            self.queue[(ts, processid)] = {"ackCounter": 1}

    def process_msg(self):
        if len(self.queue) >= 1:
            keys = self.queue.keys()  # Each key is a tuple (timestamp, processid), this allows to break ties
            keys.sort()  # Order the queue by timestamp and processid. Lowest first
            # If the element with the lowest timestamp and processid has been acknowledged by all neighbors, process it
            if self.queue[keys[0]]["ackCounter"] == len(self.neighbors):
                self.chunks.append((self.queue[keys[0]]['msg'], keys[0][0]))
                del self.queue[keys[0]]  # Delete element from queue

    def send_data(self):
        # Send data to monitor.
        self.monitor.receive_data(self.id, self.chunks)
