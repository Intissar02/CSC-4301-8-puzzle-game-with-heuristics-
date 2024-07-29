

import util
import util

class SearchProblem:
    
    #This class defines the structure of a search problem
    
    def getStartState(self):
        util.raiseNotDefined()

    def isGoalState(self, state):
        util.raiseNotDefined()

    def getSuccessors(self, state):
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        util.raiseNotDefined()

def aStarSearch(problem, heuristic):
    #A* search will prioritize the nodes with the lowest sum of the cost from the start and estimated cost to the goal

    frontier = util.PriorityQueue()
    explored = set()  #using a set for constant-time lookups
    #the start state will be pushed into the fronyier with priority 0
    startState = problem.getStartState()
    frontier.push((startState, [], 0), 0)  
#intialization of the variables to keep ttack of the expanded nodes
    expandedNodes = 0
    maxFringeSize = 0
    depth = 0
    # Loop until the frontier is empty
    while not frontier.isEmpty():
        currentState, actions, currentCost = frontier.pop()
    # Check if the current state is the goal state
        if problem.isGoalState(currentState):
            return actions, expandedNodes, maxFringeSize, depth

        if currentState not in explored:
            explored.add(currentState)
            expandedNodes += 1
            # Iterate through the successors of the current state
            for succState, succAction, succCost in problem.getSuccessors(currentState):
                newActions = actions + [succAction]
                newCost = currentCost + succCost
                if succState not in explored:
                    frontier.push((succState, newActions, newCost), newCost + heuristic(succState, problem))
                    depth = max(depth, len(newActions))

            maxFringeSize = max(maxFringeSize, frontier.count)

    return [], expandedNodes, maxFringeSize, depth


def heuristic1(state, problem=None):
    num_of_misplaced_tiles = 0
    goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    state_current = [tile for row in state.cells for tile in row]
    # Count the number of tiles not in their goal position
    for i in range(len(goal_state)):
        if state_current[i] != goal_state[i]:
            num_of_misplaced_tiles += 1

    return num_of_misplaced_tiles



def heuristic2 (state, problem=None):
    Euclidean_distance = 0
    goal_positions = {n: ((n - 1) // state.size, (n - 1) % state.size) for n in range(1, state.size * state.size)}
    goal_positions[0] = (state.size - 1, state.size - 1)  # Adjusting for 0's position in NxN
    # Calculate the Euclidean distance for each tile
    for i in range(state.size):
        for j in range(state.size):
            tile = state.cells[i][j]
            if tile != 0:
                goal_row, goal_col = goal_positions[tile]
                Euclidean_distance += ((goal_row - i) ** 2 + (goal_col - j) ** 2) ** 0.5

    return Euclidean_distance


def heuristic3 (state, problem=None):
    Manhattan_distance = 0
    goal_positions = {n: ((n - 1) // state.size, (n - 1) % state.size) for n in range(1, state.size * state.size)}
    goal_positions[0] = (state.size - 1, state.size - 1)  # Adjusting for 0's position
    # Calculate the Manhattan distance for each tile
    for i in range(state.size):
        for j in range(state.size):
            tile = state.cells[i][j]
            if tile != 0:
                goal_row, goal_col = goal_positions[tile]
                Manhattan_distance += abs(goal_row - i) + abs(goal_col - j)

    return Manhattan_distance


def heuristic4 (state, problem=None):
    out_of_row_and_column = 0
    goal_positions = {n: ((n - 1) // state.size, (n - 1) % state.size) for n in range(1, state.size * state.size)}
    goal_positions[0] = (state.size - 1, state.size - 1)
    # Count the number of tiles out of their goal row or column
    for i in range(state.size):
        for j in range(state.size):
            tile = state.cells[i][j]
            if tile != 0:
                goal_row, goal_col = goal_positions[tile]
                if goal_row != i or goal_col != j:
                    out_of_row_and_column += 1

    return out_of_row_and_column


def nullHeuristic(state, problem=None):
    """ the heuristic that always returns 0."""
    return 0
def breadthFirstSearch(problem):
        #initialization of the frontier with a queue and push the start state
    frontier = util.Queue()
    frontier.push((problem.getStartState(), [], 0))  
    explored = set()

    while not frontier.isEmpty():
        #using the FIFO, the shallowest node is poped from the frontier
        state, actions, _ = frontier.pop()

        if problem.isGoalState(state):
            return actions

        if state not in explored:
            explored.add(state)
            for successor, action, _ in problem.getSuccessors(state):
                if successor not in explored:
                    #push the successor state into the frontier
                    newActions = actions + [action]
                    frontier.push((successor, newActions, 0))

    return []
def depthFirstSearch(problem):
    """ this algorithm look for the deepest nodes in the search tree"""
    #initialization of the frontier with a stack and push the start state
    frontier = util.Stack()
    frontier.push((problem.getStartState(), [], 0))  # (state, actions, cost)
    explored = set() #the set to keep track of the explored states

    while not frontier.isEmpty():
        #using the LIFO
        state, actions, _ = frontier.pop()

        if problem.isGoalState(state):
            return actions

        if state not in explored:
            explored.add(state)
         # the loop will iterate through the successors of the current state
            for successor, action, _ in problem.getSuccessors(state):
                if successor not in explored:
                    newActions = actions + [action]
                    frontier.push((successor, newActions, 0))

    return []
#the uniform cost search function
def uniformCostSearch(problem):
    #this search function look for the node with the least total cost first
    frontier = util.PriorityQueue()
    frontier.push((problem.getStartState(), [], 0), 0)  
    explored = set()

    while not frontier.isEmpty():
        state, actions, cost = frontier.pop()
        #check if the current state is the goal state
        if problem.isGoalState(state):
            return actions
        if state not in explored:
            explored.add(state)
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in explored:
                    #append the new action to the current action
                    newActions = actions + [action]
                    newCost = cost + stepCost
                    #then it updates the priority queue with the successor state
                    frontier.update((successor, newActions, newCost), newCost)

    return []