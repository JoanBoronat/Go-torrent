from __future__ import division
from pyactor.context import interval
import matplotlib.pyplot as plt
import random


class Tracker(object):
    _tell = ['announce', 'update_peers', 'init_tracker', 'accounting']
    _ask = ['get_peers']
    _ref = ['announce', 'get_peers']

    def __init__(self):
        self.all_recieved = False
        self.accountingData = {}
        self.swarms = {}
        self.interval = ''
        self.cycle = 0

    def init_tracker(self):
        self.interval = interval(self.host, 1, self.proxy, "update_peers")

    def announce(self, torrent_hash, peer_ref):
        if torrent_hash not in self.swarms:
            self.swarms[torrent_hash] = {}
        self.swarms[torrent_hash][peer_ref] = 10

    def update_peers(self):
        self.cycle += 1
        for swarm in self.swarms:
            for peers in self.swarms[swarm].keys():
                self.swarms[swarm][peers] -= 1
                if self.swarms[swarm][peers] == 0:
                    del self.swarms[swarm][peers]

    def get_peers(self, torrent_hash, sender):
        tmp = self.swarms[torrent_hash].keys()
        if sender in tmp:
            tmp.remove(sender)
        if len(tmp) >= 6:
            return random.sample(tmp, 6)
        else:
            # print sender, "----", tmp
            return tmp

    def accounting(self, time, percentage):
        if time not in self.accountingData:
            self.accountingData[time] = 0
        self.accountingData[time] += percentage
        if self.accountingData[time] == 5 and not self.all_recieved:
            self.all_recieved = True
            aux = list()
            for val in sorted(self.accountingData.keys()):
                aux.append(self.accountingData[val] / 5)
            print "All peers received all the data. This are the mean percentages of data that peers have by gossip " \
                  "cycle: "
            aux = filter(lambda x: x > 0, aux)
            print aux

            x = range(len(aux))
            width = 1 / 1.5
            plt.bar(x, aux, width, color="blue")
            plt.savefig('foo.png')
