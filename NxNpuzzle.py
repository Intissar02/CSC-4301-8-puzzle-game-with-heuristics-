import random
from search import aStarSearch, h1, h2, h3, h4, nullHeuristic

class NxNPuzzleState:
    def __init__(self, numbers=None, size=3):
        self.size = size
        if numbers is None:
            self.cells = self.generate_solvable_puzzle()
        else:
            self.cells = [[numbers[size * i + j] for j in range(size)] for i in range(size)]
        self.blankLocation = next((i, j) for i in range(size) for j in range(size) if self.cells[i][j] == 0)

    def generate_solvable_puzzle(self):
        while True:
            puzzle = random.sample(range(self.size * self.size), self.size * self.size)
            if self.is_solvable(puzzle):
                return [[puzzle[self.size * i + j] for j in range(self.size)] for i in range(self.size)]

    def is_solvable(self, puzzle):
        inversions = sum(1 for i in range(len(puzzle)) for j in range(i + 1, len(puzzle)) if puzzle[i] > puzzle[j] and puzzle[i] != 0 and puzzle[j] != 0)
        if self.size % 2 != 0:
            return inversions % 2 == 0
        else:
            blank_row = puzzle.index(0) // self.size
            if blank_row % 2 == 0:
                return inversions % 2 != 0
            else:
                return inversions % 2 == 0

    def isGoal(self):
        goal = list(range(1, self.size * self.size)) + [0]
        return all(self.cells[i][j] == goal[i * self.size + j] for i in range(self.size) for j in range(self.size))

    def legalMoves(self):
        moves = []
        row, col = self.blankLocation
        if row > 0:
            moves.append('up')
        if row < self.size - 1:
            moves.append('down')
        if col > 0:
            moves.append('left')
        if col < self.size - 1:
            moves.append('right')
        return moves

    def result(self, move):
        row, col = self.blankLocation
        if move == 'up':
            newrow, newcol = row - 1, col
        elif move == 'down':
            newrow, newcol = row + 1, col
        elif move == 'left':
            newrow, newcol = row, col - 1
        elif move == 'right':
            newrow, newcol = row, col + 1
        else:
            raise ValueError("Illegal Move")

        newCells = [list(row) for row in self.cells]
        newCells[row][col], newCells[newrow][newcol] = newCells[newrow][newcol], newCells[row][col]
        return NxNPuzzleState(numbers=[newCells[i][j] for i in range(self.size) for j in range(self.size)], size=self.size)

    def __str__(self):
        max_width = len(str(self.size * self.size - 1))
        border = '+' + '+'.join(['=' * (max_width + 2)] * self.size) + '+'
        puzzle_str = border + "\n"
        for row in self.cells:
            row_str = "|" + "|".join(" {:^{width}} ".format(cell if cell != 0 else ' ', width=max_width) for cell in row) + "|"
            puzzle_str += row_str + "\n" + border + "\n"
        return puzzle_str.strip()

    def __eq__(self, other):
        return isinstance(other, NxNPuzzleState) and self.cells == other.cells

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.cells))


class NxNPuzzleSearchProblem:
    def __init__(self, initial):
        self.initial = initial

    def getStartState(self):
        return self.initial

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        successors = []
        for action in state.legalMoves():
            nextState = state.result(action)
            cost = 1
            successors.append((nextState, action, cost))
        return successors

    def getCostOfActions(self, actions):
        return len(actions)


if __name__ == "__main__":
    while True:
        try:
            size = int(input("Enter the puzzle dimension you want: "))
            break
        except ValueError:
            print("Invalid dimension input. Please enter an integer for the NxN puzzle dimension.")

    puzzle = NxNPuzzleState(size=size)
    print("Generated Puzzle:")
    print(puzzle)

    print("Choose a heuristic function for A* search:")
    print("1- h1 for number of misplaced tiles")
    print("2- h2 for sum of Euclidean distances of the tiles from their goal positions")
    print("3- h3 for sum of Manhattan distances of the tiles from their goal positions")
    print("4- h4 for number of tiles out of row + Number of tiles out of column")

    choice = input("Enter your choice from 1 to 4: ")
    heuristics = [nullHeuristic, h1, h2, h3, h4]
    heuristic_function = heuristics[int(choice)]

    problem = NxNPuzzleSearchProblem(puzzle)
    solution, expandedNodes, maxFringeSize, depth = aStarSearch(problem, heuristic_function)

    print(f"A* using {choice} found a path of {len(solution)} moves: {solution}")
    print(f"Expanded Nodes: {expandedNodes}")
    print(f"Max Fringe Size: {maxFringeSize}")
    print(f"Depth: {depth}")

    currentState = puzzle
    for move in solution:
        currentState = currentState.result(move)
        print(currentState)
        input("Please click to move to the next state..")
