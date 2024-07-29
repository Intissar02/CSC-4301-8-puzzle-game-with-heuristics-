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
In search.py, we implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import math

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
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

"""=====Start Change Task i=====""" 
def depthFirstSearch(problem, depth_limit=30):
    frontier = util.Stack()
    explored = set()
    frontier.push((problem.getStartState(), [], 0))  # (state, actions, current depth)
    max_fringe_size = len(frontier.list)  # Updated

    while not frontier.isEmpty():
        state, actions, current_depth = frontier.pop()
        max_fringe_size = max(max_fringe_size, len(frontier.list))  # Updated

        if current_depth > depth_limit:
            continue

        if state not in explored:
            explored.add(state)

            if problem.isGoalState(state):
                return actions, len(explored), max_fringe_size, current_depth

            for successor, action, _ in problem.getSuccessors(state):
                new_actions = actions + [action]
                frontier.push((successor, new_actions, current_depth + 1))

    return [], len(explored), max_fringe_size, 'N/A'

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    frontier = util.Queue()
    explored = set()
    frontier.push((problem.getStartState(), [], 0))
    max_fringe_size = len(frontier.list)  # changed according to the requirements

    while not frontier.isEmpty():
        state, actions, _ = frontier.pop()
        max_fringe_size = max(max_fringe_size, len(frontier.list))  # changed according to the requirements

        if state not in explored:
            explored.add(state)

            if problem.isGoalState(state):
                return actions, len(explored), max_fringe_size, len(actions)

            for successor, action, _ in problem.getSuccessors(state):
                new_actions = actions + [action]
                frontier.push((successor, new_actions, 0))

    return [], len(explored), max_fringe_size, 'N/A'


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    frontier = util.PriorityQueue()
    explored = {}
    frontier.push((problem.getStartState(), [], 0), 0)
    max_fringe_size = len(frontier.heap)   # changed according to the requirements

    while not frontier.isEmpty():
        state, actions, cost = frontier.pop()
        max_fringe_size = max(max_fringe_size, len(frontier.heap))   # changed according to the requirements

        if state not in explored or cost < explored[state]:
            explored[state] = cost

            if problem.isGoalState(state):
                return actions, len(explored), max_fringe_size, len(actions)

            for successor, action, step_cost in problem.getSuccessors(state):
                new_actions = actions + [action]
                new_cost = cost + step_cost
                frontier.update((successor, new_actions, new_cost), new_cost)

    return [], len(explored), max_fringe_size, 'N/A'

"""=====End Change Task i====="""

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

"""=====Start Change Task i=====""" 
def h1(state, problem=None):
    num_of_misplaced_tiles = 0  # initialization
    goal_state = [0, 1, 2, 3]  # the goal definition
    state_current = [tile for row in state.cells for tile in row]

    for i in range(len(goal_state)):  # the loop counts the number of tiles not in the goal position
        if state_current[i] != goal_state[i]:
            num_of_misplaced_tiles += 1

    return num_of_misplaced_tiles


def h2(state, problem=None):
    euclidean_distance = 0  # initialization
    goal_positions_mapping = {0: (1, 1), 1: (0, 0), 2: (0, 1),
                              3: (2, 1), 4: (2, 0), 5: (2, 2),
                              6: (1, 2), 7: (1, 0), 8: (0, 2)}  # the goal definition

    for i in range(3):  # the count for Euclidean distance for each tile from its goal position
        for j in range(3):
            if i < len(state.cells) and j < len(state.cells[i]):
                tile = state.cells[i][j]
                if tile != 0:
                    goal_row, goal_column = goal_positions_mapping[tile]
                    euclidean_distance += ((goal_row - i) ** 2 + (goal_column - j) ** 2) ** 0.5

    return euclidean_distance


def h3(state, problem=None):
    Manhattan_distance = 0  # initialization
    goal_positions_mapping = {0: (1, 1), 1: (0, 0), 2: (0, 1),
                              3: (2, 1), 4: (2, 0), 5: (2, 2),
                              6: (1, 2), 7: (1, 0), 8: (0, 2)}  # the goal definition
    for i in range(3):  # the count for the Manhattan distance for each tile from its goal position
        for j in range(3):
            tile = state.cells[i][j]
            if tile != 0:
                goal_row, goal_column = goal_positions_mapping[tile]
                Manhattan_distance += abs(goal_row - i) + abs(goal_column - j)

    return Manhattan_distance

def h4(state, problem=None):
    # initialization
    not_in_row = 0
    not_in_column = 0
    # the goal definition
    goal_positions_mapping = {0: (1, 1), 1: (0, 0), 2: (0, 1),
                              3: (2, 1), 4: (2, 0), 5: (2, 2),
                              6: (1, 2), 7: (1, 0), 8: (0, 2)}

    for i in range(3):  # the count of number of tiles not in the goal row and column
        for j in range(3):
            tile = state.cells[i][j]
            if tile != 0:
                goal_row, goal_column = goal_positions_mapping[tile]
                if goal_row != i:
                    not_in_row += 1
                if goal_column != j:
                    not_in_column += 1

    return not_in_row + not_in_column 
    


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # Initialize the fringe and visited set
    fringe = util.PriorityQueue()
    start = problem.getStartState()
    fringe.push((start, [], 0), heuristic(start, problem))

    visited = set()
    expandedNodes = 0
    maxFringeSize = 0
    depth = 0

    while not fringe.isEmpty():
        # Get the node with the lowest cost
        state, actions, cost = fringe.pop()

        if problem.isGoalState(state):
            return actions, expandedNodes, maxFringeSize, depth

        if state not in visited:
            visited.add(state)
            expandedNodes += 1
            depth = max(depth, len(actions))

            for nextState, action, nextCost in problem.getSuccessors(state):
                newActions = actions + [action]
                fringe.push((nextState, newActions, cost + nextCost), cost + nextCost + heuristic(nextState, problem))

            maxFringeSize = max(maxFringeSize, fringe.count)
    
    return None, 0, 0, 0  # If no solution is found

