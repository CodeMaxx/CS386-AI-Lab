import sys

class Decoder():
    directions = {
        0: 'N',
        1: 'S',
        2: 'E',
        3: 'W'
    }
    def __init__(self, gridfile):
        f = open(gridfile)
        griddata = f.read().strip().split("\n")
        self.width = len(griddata[0].split())
        self.height = len(griddata)
        states = []
        for i in griddata:
            for j in i.split():
                states.append(int(j))
        self.start = states.index(2)
        self.end = states.index(3)
        self.values = []
        self.policy = []
        f.close()

    def get_shortest_path(self, mdpfile):
        f = open(mdpfile)
        mdpdata = f.read().strip().split("\n")
        for i in mdpdata:
            if i.startswith("iteration"):
                break
            data = i.split()
            self.values.append(float(data[0]))
            self.policy.append(int(data[1]))

        state = self.start

        while(state != self.end):
            print(self.directions[self.policy[state]], end=' ')
            N = state - self.width
            S = state + self.width
            W = state - 1
            E = state + 1
            if self.policy[state] == 0:
                state = N
            elif self.policy[state] == 1:
                state = S
            elif self.policy[state] == 2:
                state = E
            elif self.policy[state] == 3:
                state = W
            else:
                print("whatwhatwhat?")

if __name__ == '__main__':
    dec = Decoder(sys.argv[1])
    dec.get_shortest_path(sys.argv[2])
