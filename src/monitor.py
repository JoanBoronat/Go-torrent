from pyactor.context import interval, later


class Monitor(object):
    _tell = ['receive_data', 'init_monitor', 'print_data', 'start_printing', 'check_data']

    def __init__(self):
        self.data = {}

    def init_monitor(self):
        later(3, self.proxy, "start_printing")
        print 'Monitor initialized'

    def start_printing(self):
        interval(self.host, 1, self.proxy, "print_data")
        interval(self.host, 5, self.proxy, "check_data")

    # Receive the data from peers
    def receive_data(self, id, chunks):
        content = map(lambda x: str(x), chunks)  # Data
        self.data[id] = reduce(lambda x, y: x + " " + y, content, "")  # Data formatted to print

    # Log the data
    def print_data(self):
        with open("log.txt", "wb") as outfile:
            for key in self.data.keys():
                outfile.write(key + "\t" + str(self.data[key]) + "\n")

    # Check that data has arrived in the correct order by all peers
    def check_data(self):
        values = self.data.values()
        m = min(map(lambda x: len(x), values))
        if m != 0:
            content = map(lambda x: x[0:m], values)  # Data
            order = all(values[i][1] <= values[i + 1][1] for i in xrange(len(values) - 1))  # Order of timestamps
            assert len(set(content)) == 1, "ERROR: Data is wrong!"  # Check all peers have the data in the same order
            assert order, "ERROR: Data is not ordered"  # Check the order of the data
            print "Data is correct!"

