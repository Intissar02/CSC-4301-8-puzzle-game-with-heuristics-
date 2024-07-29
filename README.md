8 puzzle game with heuristics 
Project Overview

This project presents an 8-puzzle solver developed as part of a coursework assignment for the course CSC 4301. The 8-puzzle is a classic problem in artificial intelligence and computer science, which involves a 3x3 grid with tiles numbered 1 through 8 and one empty space. The goal is to rearrange the tiles from an initial random configuration to the target configuration using the minimum number of moves. The project focuses on implementing various heuristic search algorithms to solve the puzzle efficiently.
Implementation Details

The solver is implemented in Python, leveraging the A* search algorithm, which combines the benefits of uniform-cost search and greedy best-first search. The project includes several heuristic functions to guide the search:

    Misplaced Tiles Heuristic (h1): Counts the number of tiles not in their goal position.
    Euclidean Distance Heuristic (h2): Calculates the sum of the Euclidean distances of the tiles from their goal positions.
    Manhattan Distance Heuristic (h3): Computes the sum of the vertical and horizontal distances of the tiles from their goal positions.
    Tiles Out of Row and Column Heuristic (h4): Counts the number of tiles out of their goal row and column.

Key Features

    Random Puzzle Generation: The program can generate a random solvable 8-puzzle configuration.
    Heuristic Choice: Users can select the heuristic function to use for the A* search.
    Visualization: The solution path is displayed, showing each move from the initial to the goal state.
    Performance Metrics: The solver provides information on the number of nodes expanded, the depth of the solution, and the runtime for each heuristic.

Results and Analysis

The performance of each heuristic is evaluated based on several metrics, including the number of nodes expanded, solution depth, and computation time. The Manhattan Distance Heuristic generally provides the best performance, balancing accuracy and computational efficiency. The project also discusses the trade-offs between different heuristics and their impact on the solver's performance.
Conclusion

This project demonstrates the application of heuristic search algorithms in solving the 8-puzzle problem. By comparing different heuristics, it highlights the importance of heuristic selection in optimizing search performance. The solver serves as an educational tool for understanding heuristic search techniques and their practical applications in problem-solving.