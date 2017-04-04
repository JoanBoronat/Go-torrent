from __future__ import division
from pyactor.context import interval
import random

import time


class Peer(object):
    _tell = ['init_peer', 'announce', 'get_peers', 'receive_peers', 'push', 'push_loop', 'pull', 'pull_loop', 'check_data', 'set_data']

    def __init__(self):
        self.torrent_hash = ''
        self.tracker = ""
        self.chunks = {}
        self.missing_chunks = []
        self.neighbors = []
        self.total_length = None
        self.assistant = None

    def init_peer(self, torrent_hash, data_lenght, protocol):
        self.tracker = self.host.lookup('tracker')
        self.torrent_hash = torrent_hash
        self.total_length = data_lenght
        self.assistant = self.host.lookup('assistant')

        # Get a list of the missing ID's
        self.missing_chunks = list(xrange(data_lenght))

        # Announce the peer every 10 seconds and get peers after that
        self.interval = interval(self.host, 10, self.proxy, "announce")

        # Check if we have all the date every second
        self.interval_check_data = interval(self.host, 1, self.proxy, "check_data")

        interval(self.host, 2, self.proxy, "get_peers")

        if protocol == "push" or protocol == "push-pull":
            # Push data among neighbors every second
            self.interval_push_data = interval(self.host, 1, self.proxy, "push_loop")

        if protocol == "pull" or protocol == "push-pull":
            # Request chunks among neighbors every second
            self.interval_pull_request = interval(self.host, 1, self.proxy, "pull_loop")

    # Announce myself to the tracker in a swarm
    def announce(self):
        self.tracker.announce(self.torrent_hash, self.proxy)

    # Get neighbors
    def get_peers(self):
        self.neighbors = self.tracker.get_peers(self.torrent_hash, self.proxy)

    def receive_peers(self, neighbors):
        self.neighbors = neighbors

    # Method to send the data to another peer
    def push(self, chunk_id, chunk_data):
        # Add the chunk if I don't have it
        if chunk_id not in self.chunks:
            self.chunks[chunk_id] = chunk_data
            self.missing_chunks.remove(chunk_id)

    # Push the data I have among my neighbors
    def push_loop(self):
        if self.chunks and self.neighbors:
            random_chunk = random.choice(self.chunks.keys())
            for neighbor in self.neighbors:
                neighbor.push(random_chunk, self.chunks[random_chunk])

    # Asking my neighbors if they have a random missing chunk
    def pull_loop(self):
        if self.missing_chunks and self.neighbors:
            random_chunk = random.choice(self.missing_chunks)
            for neighbor in self.neighbors:
                neighbor.pull(random_chunk, self.proxy)

        # If I have all the data I can stop asking for chunks
        if len(self.chunks) == self.total_length:
            # Stop pull_request
            self.interval_pull_request.set()

    # Sending the chunk if I have it
    def pull(self, chunk_id, sender):
        if chunk_id in self.chunks:
            sender.push(chunk_id, self.chunks[chunk_id])

    def set_data(self, chunks):
        self.chunks = chunks
        self.missing_chunks = []

    def check_data(self):
        self.assistant.accounting(int(time.time()), len(self.chunks) / self.total_length)
