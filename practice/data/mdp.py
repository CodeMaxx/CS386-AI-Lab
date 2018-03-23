class MDP():
    def __init__(self, file):
        f = open(file)
        self.num_states = int(f.readline())
        self.num_actions = int(f.readline())
        self.rewards = []
        for s in range(0, self.num_states):
            for a in range(0, self.num_actions):
                aRewards = list(f.readline().split())
                for sPrime in range(0, self.num_states):
                    try:
                        self.rewards[s][a].append(aRewards[sPrime])
                    except:
                        try:
                            self.rewards[s].append([aRewards[sPrime]])
                        except:
                            self.rewards.append([[aRewards[sPrime]]])

MDP("mdp-02.txt")