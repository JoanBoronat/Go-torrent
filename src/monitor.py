from pyactor.context import interval


class Monitor(object):
    _tell = ['receive_data', 'init_monitor', 'print_data']

    def __init__(self):
        self.data = {}

    def init_monitor(self):
        interval(self.host, 5, self.proxy, "print_data")
        print 'Monitor initialized'

    def receive_data(self, id, chunks):
        self.data[id] = reduce(lambda x, y: x + " " + y, chunks, "")

    def print_data(self):
        with open("log.txt", "wb") as outfile:
            for key in self.data.keys():
                outfile.write(key + "\t" + str(self.data[key]) + "\n")

