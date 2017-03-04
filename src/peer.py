import random

class Peer(object):
    _tell = ['init_peer', 'get_peers', 'announce_me', 'push', 'push_data']
    _ask = []
    _ref = ['push_data']

    def __init__(self):
        self.torrent_hash = ''
        self.tracker = ""
        self.interval = ""
        self.chunks = {}
        self.neighbors = []

    def init_peer(self, torrent_hash, data):
        self.tracker = self.host.lookup('tracker')
        self.torrent_hash = torrent_hash
        self.interval = self.host.interval(10, self.proxy, "announce_me")
        self.interval = self.host.interval(1, self.proxy, "get_peers")
        self.interval = self.host.interval(1, self.proxy, "push_data")
        if data:
            self.chunks = data

    def announce_me(self):
        self.tracker.announce(self.torrent_hash, self.proxy)

    def get_peers(self):
        self.neighbors = self.tracker.get_peers(self.torrent_hash, self.proxy)

    def push(self, chunk_id, chunk_data):
        if chunk_id not in self.chunks:
            self.chunks[chunk_id] = chunk_data
            print self.chunks

    def push_data(self):
        if self.chunks and self.neighbors:
            random_chunk = random.choice(self.chunks.keys())
            for neighbor in self.neighbors:
                neighbor.push(random_chunk, self.chunks[random_chunk])
