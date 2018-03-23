import sys

class MDP:
    def __init__(self, file):
        f = open(file)
        data = f.read().split("\n")
        self.numStates = int(data[0].split()[1])
        self.numActions = int(data[1].split()[1])
        self.start = int(data[2].split()[1])
        self.end = int(data[3].split()[1])
        self.transitions = {}
        j = 4
        while(data[j].startswith("transitions")):
            values = data[j].split()
            try:
                self.transitions[int(values[1])][int(values[2])].append((int(values[3]), float(values[4]), float(values[5])))
            except:
                try:
                    self.transitions[int(values[1])][int(values[2])] = [(int(values[3]), float(values[4]), float(values[5]))]
                except:
                    self.transitions[int(values[1])] = {int(values[2]): [(int(values[3]), float(values[4]), float(values[5]))]}
            j += 1
        self.discountFactor = float(data[j].split()[1])
        self.values = []
        self.policy = []

    def print(self):
        print(self.numStates)
        print(self.numActions)
        print(self.start)
        print(self.end)
        for s in self.transitions:
            for a in self.transitions[s]:
                for j in self.transitions[s][a]:
                    print(s, a, j)
        print(self.discountFactor)

    def _calculate_score(self, t_list):
        score = 0
        for t in t_list:
            score += t[2]*(t[1] + self.discountFactor*self.values[t[0]])
        return score

    def value_iteration(self):
        new_values = []
        for i in range(self.numStates):
            self.values.append(0.0)
            self.policy.append(-1)
            new_values.append(0.0)

        t = 0

        while True:
            for s in self.transitions:
                if s != self.end:
                    max_score = -float('inf')
                    max_action = -1
                    for a in self.transitions[s]:
                        score = self._calculate_score(self.transitions[s][a])
                        if score > max_score:
                            max_score = score
                            max_action = a
                    new_values[s] = max_score
                    self.policy[s] = max_action

            t += 1
            runagain = 0
            for s in self.transitions:
                if abs(new_values[s] - self.values[s]) > 10**-16:
                    runagain = 1
                    break

            for i in range(self.numStates):
                self.values[i] = new_values[i]

            if not runagain:
                break

        for i in range(self.numStates):
            print(round(self.values[i], 11), self.policy[i])

        print("iterations", t)

if __name__ == '__main__':
    mdp = MDP(sys.argv[1])
    mdp.value_iteration()
