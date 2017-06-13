from __future__ import division
from pyactor.context import interval, sleep
import random


class Peer(object):
    _tell = ['init_peer', 'announce', 'get_members', 'receive_peers', 'receive', 'multicast', 'join', 'leave', 'sleep',
             'send_data', 'set_sequence', 'start_multicast', 'send_msg', 'vote', 'elections']
    _ref = ['receive_peers', 'init_peer', 'elections', 'vote']
    _ask = ['get_sequence']

    def __init__(self):
        self.group_hash = ''
        self.group = None
        self.chunks = []
        self.queue = {}
        self.nextSeq = 0
        self.neighbors = []
        self.msgs = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        self.sequence = 0
        self.sequencer = None
        self.counter = 0
        self.votes = {}
        self.onElections = True

    def init_peer(self, id, url_group, group_hash):
        self.id = id
        self.group = self.host.lookup_url(url_group + 'group', 'Group', 'group')
        self.monitor = self.host.lookup_url(url_group + 'monitor', 'Monitor', 'monitor')
        self.group_hash = group_hash
        print self.id + " initialized"

    def join(self):
        self.group.join(self.group_hash)
        self.interval = interval(self.host, 10, self.proxy, "announce")  # Keep alive
        self.interval_members = interval(self.host, 1, self.proxy, "get_members")
        # If i'm not the sequencer, send data
        self.interval_multicast = interval(self.host, 1, self.proxy, "multicast")
        self.interval_data = interval(self.host, 1, self.proxy, "send_data")  # Monitoring data

    def leave(self):
        self.group.leave(self.group_hash, self.proxy)

    # Announce myself to the group
    def announce(self):
        self.group.announce(self.group_hash, self.proxy)

    # Get neighbors (asynchronous call)
    def get_members(self):
        self.group.get_members(self.group_hash, self.proxy)

    # Receive the requested neighbors once they are all announced to the group
    def receive_peers(self, neighbors):
        self.neighbors = neighbors
        self.interval_members.set()  # Stop asking for neighbors
        sleep(3)
        self.elections()

    # Receive the data from another peer
    def receive(self, m, seq):
        # If the msg received is the next expected process it, otherwise queue it
        if seq == self.nextSeq:
            self.process_msg(m, seq)
        else:
            self.queue[seq] = m

    # Push the data I have to a random neighbor
    def multicast(self):
        if self.neighbors and not self.onElections and self.sequencer:
            try:
                seq = self.sequencer.get_sequence(timeout=5)  # Ask for a sequence.
                self.send_msg(seq)
            except:
                self.onElections = True
                self.elections()  # If the timeout is reached start elections

    def send_msg(self, seq):
        m = random.choice(self.msgs)
        self.receive(m, seq)
        sleep(random.random())  # Force disorder
        map(lambda x: x.receive(m, seq), self.neighbors)  # Sending msg to my neighbors

    # Elect the new sequencer
    def elections(self):
        if self.sequencer:
            self.neighbors.remove(self.sequencer)  # Remove the sequencer from neighbors
        aux = self.neighbors[:]  # List of alive neighbors
        aux.append(self.proxy)  # Append myself to the list of candidates
        aux.sort()  # Sort the list
        elected = aux[0]  # The lowest ID wins
        map(lambda x: x.vote(elected), self.neighbors)  # Sending vote to my neighbors

    def vote(self, election):
        if election in self.votes:
            self.votes[election] += 1
        else:
            self.votes[election] = 1
        # If everyone has voted the peer with more votes wins
        if sum(self.votes.values()) == len(self.neighbors):
            self.sequencer = max(self.votes, key=self.votes.get)
            if self.sequencer != self.proxy:
                self.onElections = False
            else:
                print self.id, "I've been elected!"
            self.votes = {}

    def process_msg(self, m, seq):
        self.chunks.append((m, seq))  # Msg processed
        self.nextSeq += 1
        # If the next expected msg is in the queue process it
        if self.nextSeq in self.queue.keys():
            m = self.queue[self.nextSeq]
            del self.queue[self.nextSeq]
            self.process_msg(m, self.nextSeq)

    def get_sequence(self):
        self.sequence += 1
        return self.sequence - 1

    def send_data(self):
        # Send data to monitor
        self.monitor.receive_data(self.id, self.chunks)

    def sleep(self, n):
        sleep(n)