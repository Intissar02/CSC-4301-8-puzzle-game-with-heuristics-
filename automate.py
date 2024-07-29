import csv
from eightpuzzle import EightPuzzleState, EightPuzzleSearchProblem, createRandomEightPuzzle
from search import aStarSearch, h1, h2, h3, h4
from statistics import mean
from tabulate import tabulate
from multiprocessing import Process, Queue
import time

def run_search_algorithm(problem, heuristic_function, result_queue):
    """
    the function to run the search algorithm and put the result in the queue.
    """
    start_time = time.time()
    result = aStarSearch(problem, heuristic_function)
    end_time = time.time()
    execution_time = end_time - start_time
    result_queue.put(result + (execution_time,))

def generate_random_puzzles(filename, num_puzzles=20):
    """
    the generation of a  random puzzle configurations and save them to a file.
    """
    with open(filename, 'w') as file:
        for _ in range(num_puzzles):
            puzzle = createRandomEightPuzzle()
            config = [puzzle.cells[row][col] for row in range(3) for col in range(3)]
            config_str = ' '.join(map(str, config))
            file.write(config_str + '\n')

# Read puzzle configurations from a file.

def read_puzzle_configurations(filename):

    configurations = []
    with open(filename, 'r') as file:
        for line in file:
            config = [int(n) for n in line.strip().split()]
            configurations.append(config)
    return configurations

def main():
    generate_random_puzzles('scenarios.csv')
#the generation of the puzzle taking into consideration the expanded nodes, the max fring size, and execution time
    configurations = read_puzzle_configurations('scenarios.csv')
    heuristics = [h1, h2, h3, h4]
    results = {heuristic.__name__: {'Nodes Expanded': [], 'Max Fringe Size': [], 'Execution Time': []} for heuristic in heuristics}

    timeout = 60 

    with open('results.csv', 'w', newline='') as results_file:
        results_writer = csv.writer(results_file)
        results_writer.writerow(['Initial State', 'Heuristic', 'Expanded Nodes', 'Max Fringe Size', 'Depth', 'Execution Time'])

        for config in configurations:
            puzzle = EightPuzzleState(config)
            problem = EightPuzzleSearchProblem(puzzle)

            for heuristic_function in heuristics:
                result_queue = Queue()
                process = Process(target=run_search_algorithm, args=(problem, heuristic_function, result_queue))
                process.start()

                # Wait for the process to finish or timeout
                process.join(timeout)

                if process.is_alive():
                    print(f"Timeout occurred for configuration {config} with heuristic {heuristic_function.__name__}")
                    process.terminate()
                    process.join()
                    results_writer.writerow([' '.join(map(str, config)), heuristic_function.__name__, "Timeout", "Timeout", "Timeout", "Timeout"])
                else:
                    path, nodes_expanded, max_fringe_size, depth, execution_time = result_queue.get()
                    results[heuristic_function.__name__]['Nodes Expanded'].append(nodes_expanded)
                    results[heuristic_function.__name__]['Max Fringe Size'].append(max_fringe_size)
                    results[heuristic_function.__name__]['Execution Time'].append(execution_time)
                    results_writer.writerow([' '.join(map(str, config)), heuristic_function.__name__, nodes_expanded, max_fringe_size, depth, execution_time])
                               
    # Calculating the averages from the heuristics
    averages = {heuristic: {
        'Avg Nodes Expanded': mean(metrics['Nodes Expanded']),
        'Avg Max Fringe Size': mean(metrics['Max Fringe Size']),
        'Avg Execution Time': mean(metrics['Execution Time'])
    } for heuristic, metrics in results.items()}

    # ranking the heuristics based on average nodes expanded
    ranked_heuristics = sorted(averages.keys(), key=lambda x: averages[x]['Avg Nodes Expanded'])

    # Display results
    headers = ["Heuristic", "Avg Nodes Expanded", "Avg Max Fringe Size", "Avg Execution Time"]
    rows = [[heuristic, averages[heuristic]['Avg Nodes Expanded'], averages[heuristic]['Avg Max Fringe Size'], averages[heuristic]['Avg Execution Time']] for heuristic in ranked_heuristics]
    print("\nAverage Results:")
    print(tabulate(rows, headers=headers, tablefmt="grid"))

    print("\nRanking of Heuristics Based on Average Expanded Nodes:")
    for rank, heuristic in enumerate(ranked_heuristics, start=1):
        print(f"Rank {rank}: {heuristic}")

if __name__ == "__main__":
    main()
