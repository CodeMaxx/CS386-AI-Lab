# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


class Node:
    def __init__(self, successor, parent=None):
        self.state = successor[0]
        self.parent = parent
        self.action = successor[1]

        if parent is not None:
            self.cost = parent.cost + successor[2]
        else:
            self.cost = 0

    def reconstructPath(self):
        path = []
        node = self
        while node.parent is not None:
            path = [node.action] + path
            # print node.parent.state
            node = node.parent
        # print path
        return path

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    # print "I am in DFS"

    frontier = util.Stack()
    explored = []

    rootNode = Node((problem.getStartState(), None, None))

    frontier.push(rootNode)

    # print "I pushed rootNode to frontier"

    while not frontier.isEmpty():
        nextNode = frontier.pop()
        # print "this loop", nextNode.state
        if(problem.isGoalState(nextNode.state)):
            return nextNode.reconstructPath()

        explored.append(nextNode.state)

        for successor in problem.getSuccessors(nextNode.state):
            if successor[0] not in explored: # TODO - Also check not in frontier
                frontier.push(Node(successor, nextNode))

    print "No solution found by DFS"
    return []

    "*** YOUR CODE HERE ***"

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    frontier = util.Queue()
    explored = []

    rootNode = Node((problem.getStartState(), None, None))

    frontier.push(rootNode)

    # print "I pushed rootNode to frontier"

    frontier_list = []

    frontier_list.append(rootNode.state)

    while not frontier.isEmpty():
        nextNode = frontier.pop()
        frontier_list.remove(nextNode.state)
        # print "this loop", nextNode.state
        if(problem.isGoalState(nextNode.state)):
            return nextNode.reconstructPath()

        explored.append(nextNode.state)

        for successor in problem.getSuccessors(nextNode.state):
            if successor[0] not in explored  and successor[0] not in frontier_list:
                frontier.push(Node(successor, nextNode))
                frontier_list.append(successor[0])

    print "No solution found by BFS"
    return []

    "*** YOUR CODE HERE ***"

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    frontier = util.PriorityQueue()
    explored = []

    rootNode = Node((problem.getStartState(), None, None))

    frontier.push(rootNode, rootNode.cost)

    # print "I pushed rootNode to frontier"

    frontier_list = []

    frontier_list.append(rootNode.state)

    while not frontier.isEmpty():
        nextNode = frontier.pop()
        frontier_list.remove(nextNode.state)
        # print "this loop", nextNode.state
        if(problem.isGoalState(nextNode.state)):
            return nextNode.reconstructPath()

        explored.append(nextNode.state)

        for successor in problem.getSuccessors(nextNode.state):
            if successor[0] not in explored  and successor[0] not in frontier_list:
                newNode = Node(successor, nextNode)
                frontier.push(newNode, newNode.cost)
                frontier_list.append(successor[0])

    print "No solution found by UCS"
    return []

    "*** YOUR CODE HERE ***"

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    def prioFunc(node, heuristic=heuristic):
        # print (node.cost + heuristic(node.state, problem))
        return node.cost + heuristic(node.state, problem)

    frontier = util.PriorityQueue()
    explored = []

    rootNode = Node((problem.getStartState(), None, None))

    frontier.push(rootNode, prioFunc(rootNode))

    # print "I pushed rootNode to frontier"

    frontier_list = []

    frontier_list.append(rootNode.state)

    done_list = []

    while not frontier.isEmpty():
        nextNode = frontier.pop()
        
        if nextNode.state in explored:
            continue

        # print nextNode.state
        frontier_list.remove(nextNode.state)
        # print "this loop", nextNode.state
        if(problem.isGoalState(nextNode.state)):
            return nextNode.reconstructPath()

        explored.append(nextNode.state)

        for successor in problem.getSuccessors(nextNode.state):
            if successor[0] not in explored:
                newNode = Node(successor, nextNode)
                frontier.update(newNode, prioFunc(newNode))
                frontier_list.append(successor[0])

    print "No solution found by aStar"
    return []

    "*** YOUR CODE HERE ***"


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
