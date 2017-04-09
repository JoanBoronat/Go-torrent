import matplotlib.pyplot as plt
from pyactor.context import interval
import numpy as np
import sys


# Assistant is a peer that will manage all the accounting of the torrent and sets the seed.
class Assistant(object):
    _tell = ['init_assistant', 'accounting', 'load_file', 'print_data', 'print_data_start']
    _ref = ['load_file']

    def __init__(self):
        self.all_received = False
        self.num_peers = 0
        self.accountingData = {"0": 0}
        self.total_length = 0
        self.protocol = None
        self.interval_print_data = None

    def init_assistant(self, num_peers, total_length, protocol):
        self.num_peers = num_peers
        self.total_length = total_length
        self.protocol = protocol

    # Saves the statistics of the peers
    def accounting(self, t, percentage):
        if (max(self.accountingData.values()) / self.num_peers * 100) != 100:
            if t not in self.accountingData:
                self.accountingData[t] = 0
            self.accountingData[t] += percentage

    # Reads the content of the file with the data and sets de seed peer.
    def load_file(self, peer):
        f = open("../file.txt")

        # Read file
        l = list(f.read())

        # Split the file into equally sized chunks.
        l = list(np.array_split(l, self.total_length))

        # Convert the arrays to strings
        l = map(''.join, l)
        k = range(len(l))
        peer.set_data(dict(zip(k, l)))

    # Print the counter of the data received and plots the graph.
    def print_data(self):
        sys.stdout.write("\r%s%d%%" % ("Average percentage of data received: ",
                                       (max(self.accountingData.values()) / self.num_peers * 100)))
        sys.stdout.flush()

        if (max(self.accountingData.values()) / self.num_peers * 100) == 100:
            print "\nAll peers received all the data. You can find a graph with the statistics here src/" + \
                  self.protocol + ".png"
            self.interval_print_data.set()

            aux = list()
            for val in sorted(self.accountingData.keys()):
                aux.append(self.accountingData[val] / self.num_peers)
            aux = filter(lambda x: x > 0, aux)
            aux = map(lambda x: x * 100, aux)

            x = range(len(aux))
            plt.plot(x, aux)
            plt.ylabel('Percentage of data received')
            plt.xlabel('Gossip cycle')
            plt.title("Accounting of " + self.protocol + " protocol with " + str(self.num_peers) + " peers")
            plt.savefig(self.protocol + '.png')

    # Starts the accounting interval
    def print_data_start(self):
        print ""
        self.interval_print_data = interval(self.host, 1, self.proxy, "print_data")
