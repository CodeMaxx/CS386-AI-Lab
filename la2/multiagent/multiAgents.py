# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        points = successorGameState.getScore()

        if successorGameState.isWin():
          return float('inf')

        if successorGameState.isLose():
          return - float('inf')

        points += (currentGameState.getNumFood() - successorGameState.getNumFood()) * 200

        capsulePositions = currentGameState.getCapsules()

        for i in capsulePositions:
          if i == newPos:
            points += 100

        minFoodDistance = float('inf')

        for i in newFood.asList():
          dist = manhattanDistance(i, newPos)
          if dist < minFoodDistance:
            minFoodDistance = dist

        points -= minFoodDistance*5

        newGhostPositions = successorGameState.getGhostPositions()

        for i in range(len(newGhostPositions)):
          dist = manhattanDistance(newPos, newGhostPositions[i])
          if dist == 0 and newScaredTimes[i] != 0:
            points += 1000
          elif dist < 4:
            if newScaredTimes[i] != 0:
              # print newScaredTimes[i]
              points += 500
            else:
              points -= 500

        if action == Directions.STOP:
          points -= 10

        return points

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        def minfunc(state, depth, agentIndex):
          if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state)

          v = float("inf")

          numAgents = state.getNumAgents()

          legalMoves = state.getLegalActions(agentIndex)

          for move in legalMoves:
            if agentIndex == numAgents - 1:
              v = min(v, maxfunc(state.generateSuccessor(agentIndex, move), depth - 1))
            else:
              v = min(v, minfunc(state.generateSuccessor(agentIndex, move), depth, agentIndex + 1))

          return v


        def maxfunc(state, depth):
          if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state)

          v = - float("inf")

          legalMoves = state.getLegalActions(0)

          for move in legalMoves:
            v = max(v, minfunc(state.generateSuccessor(0, move), depth, 1))

          return v

        legalMoves = gameState.getLegalActions(0)

        if gameState.isWin() or gameState.isLose() or self.depth == 0:
          return self.evaluationFunction(gameState)

        bestmove = Directions.STOP
        v = - float('inf')

        for move in legalMoves:
          score = minfunc(gameState.generateSuccessor(0, move), self.depth, 1)
          if score > v:
            v = score
            bestmove = move

        return bestmove


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        def minfunc(state, depth, agentIndex, alpha, beta):
          if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state)

          v = float("inf")

          numAgents = state.getNumAgents()

          legalMoves = state.getLegalActions(agentIndex)

          for move in legalMoves:
            if agentIndex == numAgents - 1:
              v = min(v, maxfunc(state.generateSuccessor(agentIndex, move), depth - 1, alpha, beta))
            else:
              v = min(v, minfunc(state.generateSuccessor(agentIndex, move), depth, agentIndex + 1, alpha, beta))
            if v < alpha:
              return v
            beta = min(beta, v)

          return v


        def maxfunc(state, depth, alpha, beta):
          if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state)

          v = - float("inf")

          legalMoves = state.getLegalActions(0)

          for move in legalMoves:
            v = max(v, minfunc(state.generateSuccessor(0, move), depth, 1, alpha, beta))
            if v > beta:
              return v
            alpha = max(alpha, v)

          return v

        alpha = - float('inf')
        beta = float('inf')
        legalMoves = gameState.getLegalActions(0)

        if gameState.isWin() or gameState.isLose() or self.depth == 0:
          return self.evaluationFunction(gameState)

        bestmove = Directions.STOP
        v = - float('inf')

        for move in legalMoves:
          score = minfunc(gameState.generateSuccessor(0, move), self.depth, 1, alpha, beta)

          if score > v:
            v = score
            bestmove = move

          if v > beta:
            return bestmove
          alpha = max(alpha, v)

        return bestmove


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:
      So here's goes my story. Winning is the ultimate goal (inf) and losing is the ultimate defeat (-inf).
      Food is good. I want food. The current score captures the essense of eating food but has no incentive
      to go closer to eat it. For this I find the minimum distance from food and take away points if we are
      far. As good as it feels to keep eating all the time, life is not this easy. Everyone has their share of
      problems and pacman is not special. There are ghosts roaming around in town trying to find pacman, kill
      him and make him one of them. A state close to (manhattan distance) the ghosts is not a good state.
      Negative points for getting close. Then comes a twist. There are magic capsule hidden in town. When pacman
      eats the capsule, ghosts become weak and vulnerable to attack. Nobody messes with pacman. Killing ghosts
      (oh the irony!) as well as going closer to a vulnerable ghost has been incentivised. Taking our heuristics
      and his artificial intelligence pacman goes on the rule the town!  
      

      Interesting stuff:
      1. So incentivising going closer to food has one negative. When you eat a pellet, the minimum distance
      suddenly increases. Thus there is a fight between the increase in points due to eating and the penalty
      due to increase in distance. I had to play around with the constants to get this right.
      2. Trying to eat ghosts increases the time pacman spends near the capsules. This wastes time leading to
      a decrease in the score. Thus there is a fight between time and eating ghosts.
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # Current game score
    points = currentGameState.getScore()*5

    # Winning is important
    if currentGameState.isWin():
      return float('inf')

    # Can't afford to lose
    if currentGameState.isLose():
      return - float('inf')

    minFoodDistance = float('inf')

    if len(newFood.asList()) == 0:
      minFoodDistance = 0

    for i in newFood.asList():
      # Getting distance from food
      dist = manhattanDistance(i, newPos)
      if dist < minFoodDistance:
        minFoodDistance = dist

    # Decrese in mininum distance from food incentivises going close to food
    points -= minFoodDistance*5

    newGhostPositions = currentGameState.getGhostPositions()

    for i in range(len(newGhostPositions)):
      # Getting distance from ghost
      dist = manhattanDistance(newPos, newGhostPositions[i])
      if dist == 0 and newScaredTimes[i] != 0:
        # Eating ghosts is cool!
        # Giving points to eat ghosts
        points += 500
        # If distance from ghost is >= 4 then we really don't need to worry
      elif dist < 4:
        # If the ghost is closer than manhattan distance 4 and still has scared time left, lets go get it ;)
        if newScaredTimes[i] > 5:
          # The closer we are the more points we get
          points += (4 - dist) * 200
        # Beware! Ghosts can kill!
        # subtract points if we're too close to a ghost - prevents getting killed
        else:
          points -= 500 

    return points

# Abbreviation
better = betterEvaluationFunction

