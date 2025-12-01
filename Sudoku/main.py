import time, copy
from parsing import parse_sudoku_file, boards_match
from solver_backtracking import solve_backtracking
from solver_mrv import solve_mrv
from solver_unit_prop import solve_unit_prop
from solver_cbj import solve_backjumping

def run_benchmark():
    puzzles = parse_sudoku_file("Sudoku_Dataset/sudoku95test.txt")
    solutions = parse_sudoku_file("Sudoku_Dataset/soln_raw.txt")

    if len(puzzles) != len(solutions):
        print("Error: mismatch puzzle counts")
        return

    solvers = [
        ("Naive Backtracking", solve_backtracking),
        ("Backtracking + MRV", solve_mrv),
        ("Unit Propagation", solve_unit_prop),
        ("Backjumping (CBJ)", solve_backjumping)
    ]

    print(f"Running {len(puzzles)} puzzles...")

    for name, solver in solvers:
        total = 0; correct = 0
        cp = copy.deepcopy(puzzles)
        print(name)
        start = time.time()

        for i,p in enumerate(cp):
            solver(p)
            if boards_match(p, solutions[i]):
                correct += 1

        total = time.time() - start
        print(f"  Correct: {correct}/{len(cp)} | Time: {total:.3f}s")

if __name__ == "__main__":
    run_benchmark()
