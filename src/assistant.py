import matplotlib.pyplot as plt
import numpy as np


class Assistant(object):
    _tell = ['init_assistant', 'accounting', 'load_file']
    _ref = ['load_file']

    def __init__(self):
        self.all_received = False
        self.num_peers = 0
        self.accountingData = {}
        self.total_length = 0
        self.protocol = None

    def init_assistant(self, num_peers, total_length, protocol):
        self.num_peers = num_peers
        self.total_length = total_length
        self.protocol = protocol

    def accounting(self, time, percentage):
        if time not in self.accountingData:
            self.accountingData[time] = 0
        self.accountingData[time] += percentage
        if self.accountingData[time] == self.num_peers and not self.all_received:
            self.all_received = True
            aux = list()
            for val in sorted(self.accountingData.keys()):
                aux.append(self.accountingData[val] / self.num_peers)
            print "All peers received all the data. This are the mean percentages of data that peers have by gossip " \
                  "cycle: "
            aux = filter(lambda x: x > 0, aux)
            aux = map(lambda x: x * 100, aux)
            print aux

            x = range(len(aux))
            y = range(10, 110, 10)
            width = 1 / 1.5
            plt.bar(x, aux, width, color="#d8721e")
            plt.ylabel('Percentage of received data')
            plt.yticks(y, ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"])
            plt.xlabel('Gossip cycle')
            plt.title("Accounting gossip with " + self.protocol + " protocol")
            plt.savefig('foo.png')

    def load_file(self, peer):
        f = open("../file.txt")

        # Read file
        l = list(f.read())

        # Split the file into equaly sized chunks.
        l = list(np.array_split(l, self.total_length))

        # Convert the arrays to strings
        l = map(''.join, l)
        k = range(len(l))

        peer.set_data(dict(zip(k, l)))
