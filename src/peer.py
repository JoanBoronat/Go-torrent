class Peer(object):
    _tell = ['init_peer', 'get_peers', 'announce_me']
    _ask = []

    def __init__(self):
        self.torrent_hash = {}
        self.tracker = ""
        self.interval = ''

    def init_peer(self, torrent_hash):
        self.tracker = self.host.lookup('tracker')
        self.torrent_hash = torrent_hash
        self.interval = self.host.interval(10, self.proxy, "announce_me")

    def announce_me(self):
        self.tracker.announce(self.torrent_hash, self.proxy)

    def get_peers(self):
        print self.tracker.get_peers(self.torrent_hash)