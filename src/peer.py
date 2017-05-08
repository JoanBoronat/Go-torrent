from __future__ import division
from pyactor.context import interval
import random
import time


class Peer(object):
    _tell = ['init_peer', 'announce', 'get_members', 'receive_peers', 'push', 'push_data', 'pull_data', 'pull',
             'check_data', 'set_data', 'join']
    _ref = ['receive_peers']

    def __init__(self):
        self.torrent_hash = ''
        self.group = ""
        self.chunks = {}
        self.missing_chunks = []
        self.neighbors = []
        self.total_length = None
        self.assistant = None

    def init_peer(self, url_group, url_assistant, torrent_hash, data_lenght, protocol):
        self.group = self.host.lookup_url(url_group + 'group', 'Group', 'group')
        self.assistant = self.host.lookup_url(url_assistant + 'assistant', 'Assistant', 'assistant')
        self.torrent_hash = torrent_hash
        self.total_length = data_lenght

        # Get a list of the missing ID's
        self.missing_chunks = list(xrange(data_lenght))

        self.join()

        # Check the data for accounting
        self.interval_check_data = interval(self.host, 1, self.proxy, "check_data")

        interval(self.host, 2, self.proxy, "get_members")

        if protocol == "push" or protocol == "push-pull":
            # Push data among neighbors every second
            self.interval_push_data = interval(self.host, 1, self.proxy, "push_data")

        if protocol == "pull" or protocol == "push-pull":
            # Request chunks among neighbors every second
            self.interval_pull_request = interval(self.host, 1, self.proxy, "pull")

    def join(self):
        self.group.join(self.torrent_hash, self.proxy)
        # Announce the peer every 10 seconds
        self.interval = interval(self.host, 10, self.proxy, "announce")

    def leave(self):
        self.group.leave(self.torrent_hash, self.proxy)

    # Announce myself to the group in a swarm
    def announce(self):
        self.group.announce(self.torrent_hash, self.proxy)

    # Get neighbors (asynchronous call)
    def get_members(self):
        self.neighbors = self.group.get_members(self.torrent_hash, self.proxy)

    # Receive the requested peers
    def receive_peers(self, neighbors):
        self.neighbors = neighbors

    # Receive the push from another peer
    def push(self, chunk_id, chunk_data):
        # Add the chunk if I don't have it
        if chunk_id not in self.chunks:
            self.chunks[chunk_id] = chunk_data
            self.missing_chunks.remove(chunk_id)

    # Push the data I have to a random neighbor
    def push_data(self):
        if self.chunks and self.neighbors:
            random_chunk = random.choice(self.chunks.keys())
            neighbor = random.choice(self.neighbors)
            neighbor.push(random_chunk, self.chunks[random_chunk])

    # Asking a neighbor if he has one of my missing chunks (asynchronous call)
    def pull(self):
        if self.missing_chunks and self.neighbors:
            neighbor = random.choice(self.neighbors)
            neighbor.pull_data(random.choice(self.missing_chunks), self.proxy)

        elif not self.missing_chunks:
            self.interval_pull_request.set()

    # Sending the chunk if I have it
    def pull_data(self, chunk_id, sender):
        if chunk_id in self.chunks:
            sender.push(chunk_id, self.chunks[chunk_id])

    def set_data(self, chunks):
        self.chunks = chunks
        self.missing_chunks = []

    def check_data(self):
        self.assistant.accounting(int(time.time()), len(self.chunks) / self.total_length)
