import random
import numpy as np


class Peer(object):
    _tell = ['init_peer', 'announce_me', 'push', 'push_data', 'load_file', 'pull_request', 'pull', 'get_peers', 'check_data']
    _ref = ['push_data']

    def __init__(self):
        self.torrent_hash = ''
        self.tracker = ""
        self.chunks = {}
        self.missing_chunks = None
        self.neighbors = []
        self.total_lengh = None

    def init_peer(self, torrent_hash, data_lenght):
        self.tracker = self.host.lookup('tracker')
        self.torrent_hash = torrent_hash
        self.total_lengh = data_lenght

        #Get a list of the missing ID's
        self.missing_chunks = list(xrange(data_lenght))

        # Announce the peer every 10 seconds and get peers after that
        self.interval = self.host.interval(10, self.proxy, "announce_me")
        self.host.later(1, self.proxy, "get_peers")

        # Push data among neighbors every second
        self.interval_push_data = self.host.interval(1, self.proxy, "push_data")

        # Request chunks among neighbors everey second
        self.interval_pull_request = self.host.interval(1, self.proxy, "pull_request")

        # Check if we have all the date every second
        self.interval_check_data = self.host.interval(1, self.proxy, "check_data")

    # Announce myself to the tracker in a swarm
    def announce_me(self):
        self.tracker.announce(self.torrent_hash, self.proxy)

    # Get neighbors
    def get_peers(self):
        self.neighbors = self.tracker.get_peers(self.torrent_hash, self.proxy)

    # Method to send the data to another peer
    def push(self, chunk_id, chunk_data):
        # Add the chunk if I don't have it
        if chunk_id not in self.chunks:
            self.chunks[chunk_id] = chunk_data
            self.missing_chunks.remove(chunk_id)

    # Push the data I have among my neighbors
    def push_data(self):
        if self.chunks and self.neighbors:
            random_chunk = random.choice(self.chunks.keys())
            for neighbor in self.neighbors:
                neighbor.push(random_chunk, self.chunks[random_chunk])

    # Asking my neighbors if they have a random missing chunk
    def pull_request(self):
        if self.missing_chunks and self.neighbors:
            random_chunk = random.choice(self.missing_chunks)
            for neighbor in self.neighbors:
                neighbor.pull(random_chunk, self.proxy)

    # Sending the chunk if I have it
    def pull(self, chunk_id, sender):
        if chunk_id in self.chunks:
            sender.push(chunk_id, self.chunks[chunk_id])

    def check_data(self):
        # If I have all the data I can stop asking for chunks
        if len(self.chunks) == self.total_lengh:
            # Stop pull_request
            self.interval_pull_request.set()
            self.interval_check_data.set()
            print self.id, ", I've got all the data! Here is what I recieved: ", self.chunks.values()

    def load_file(self):
        nChunks = 9
        f = open("../file.txt")

        # Read file
        l = list(f.read())

        # Split the file into equaly sized chunks.
        l = list(np.array_split(l, nChunks))

        # Convert the arrays to strings
        l = map((lambda x: ''.join(x)), l)
        k = range(len(l))
        self.chunks = dict(zip(k, l))




