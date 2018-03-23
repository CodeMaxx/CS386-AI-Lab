import sys
from enum import Enum

class Action(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

    def __str__(self):
        return str(self.value)

class Encoder:
    numActions = 4

    def __init__(self, file):
        f = open(file)
        data = f.read().strip().split("\n")
        self.width = len(data[0].split())
        self.height = len(data)
        self.states = []
        t = 0
        for i in data:
            for j in i.split():
                self.states.append(int(j))
        self.start = self.states.index(2)
        self.end = self.states.index(3)
        self.discountFactor = 1

    def get_numstates(self):
        return self.width * self.height

    def print_grid(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.states[i*self.width + j], " ", end='')
            print("\n")

    def _print_transitions(self, s):
        if self.states[s] == 1:
            return
        N = s - self.width
        S = s + self.width
        W = s - 1
        E = s + 1

        if self.states[N] != 1:
            print("transitions", s, Action.NORTH, N, -1, 1)
        if self.states[S] != 1:
            print("transitions", s, Action.SOUTH, S, -1, 1)
        if self.states[W] != 1:
            print("transitions", s, Action.WEST, W, -1, 1)
        if self.states[E] != 1:
            print("transitions", s, Action.EAST, E, -1, 1)

    def dump(self):
        print("numStates", self.get_numstates())
        print("numActions", self.numActions)
        print("start", self.start)
        print("end", self.end)
        for i in range(self.get_numstates()):
            self._print_transitions(i)
        print("discount ", self.discountFactor)

if __name__ == '__main__':
    encoded = Encoder(sys.argv[1])
    # encoded.print_grid()
    encoded.dump()