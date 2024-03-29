##############################################
#                                            #
# Authors: Jorge de Miguel Pires             #
#          jorge.miguelp@estudiante.uam.es   #
#                                            #
#          Laura de Paz Carbajo              #
#          laura.pazc@estudiante.uam.es      #
# Team 07                                    #
# Group 2351                                 #
#                                            #
##############################################


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
    This class outlines the structure of a search problem,
    but doesn't implement any of the methods
    (in object-oriented terminology: an abstract class).

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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:",problem.getSuccessors(problem.getStartState()))
    """

    return generalSearch(problem, util.Stack())


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    return generalSearch(problem, util.Queue())


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    return generalSearch(problem, util.PriorityQueue(), True)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the
    nearest goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    return generalSearch(problem, util.PriorityQueue(), True, heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


###########################################
# generalSearch: function that generalizes
# all the search problems
###########################################
def generalSearch(problem, opened, cost=None, heuristic=nullHeuristic):
    root = problem.getStartState()
    rootNode = Node(root, "Stop", 0, None)

    # Depending on the structure it uses different costs
    if cost is None:
        opened.push(rootNode)
    else:
        cost = 0
        opened.push(rootNode, cost)

    closed = []
    sol = []

    # Iterate
    while not opened.isEmpty():
        # Choose from opened list a node to expand
        node = opened.pop()
        nodePos, nodeAct, nodeCost = node.getTuple()

        if problem.isGoalState(nodePos):
            # Creates and returns lists of actions
            while node.getParent() is not None:
                sol.append(node.getTuple()[1])
                node = node.getParent()

            sol.reverse()
            return sol

        if node not in closed:
            closed.append(node)

            # Expand node
            for succ in problem.getSuccessors(nodePos):
                nodeSucc = Node(succ[0], succ[1], nodeCost + succ[2], node)
                if nodeSucc not in closed:
                    # Push the successor to the opened list
                    if cost is None:
                        opened.push(nodeSucc)
                    else:
                        heur = heuristic(succ[0], problem)
                        cost = nodeSucc.getTuple()[2] + heur
                        opened.push(nodeSucc, cost)

    return False


####################################
# Node: a node of the search tree
# with a link to his parent node,
# the action to get to the node and
# the cost of the action
####################################
class Node:
    def __init__(self, node, action, cost, parent):
        self.info = node
        self.action = action
        self.cost = cost
        self.parent = parent

    def __eq__(self, node):
        return self.info == node.info

    def __str__(self):
        return "Node: " + str(self.info) + ", " + \
                self.action + ", " + str(self.cost)

    def getTuple(self):
        return self.info, self.action, self.cost

    def getParent(self):
        return self.parent
