# SAT & Constraint Satisfaction Project

This project implements various Constraint Satisfaction Problem (CSP) and Boolean Satisfiability (SAT) solvers. It includes implementations for solving **SAT problems** (CNF format), **Sudoku puzzles**, and a **Minesweeper** bot using logic inference.

## Project Structure

The project is divided into three main modules:

1.  **SAT/**: Core SAT solvers for DIMACS CNF files.
2.  **Sudoku/**: Sudoku solvers comparing different heuristics.
3.  **Bonus/**: A Minesweeper solver using a SAT-based approach (DPLL).

## Prerequisites

* **Python 3.10** or higher.
* No external packages (`pip install`) are required. This project uses the Python Standard Library (`multiprocessing`, `unittest`, `random`, `sys`, `os`, `copy`).

---

## 1. SAT Solvers

This module implements four different algorithms to solve 3-SAT problems:
* **Naive Backtracking**
* **Degree Heuristic**
* **DPLL (Davis–Putnam–Logemann–Loveland) with Unit Propagation**
* **Conflict-Directed Backjumping (CBJ)**

### Running the SAT Benchmark
The project comes with a pre-populated dataset of Random 3-SAT and Pigeonhole Principle problems in the `SAT_Dataset/` directory.

To run the solvers against these files, navigate to the `SAT` directory and run the benchmark script:

```bash
cd SAT
python sat_benchmark.py

This script will run all four solvers against the .cnf files and output the execution time and solution validity.

2. Sudoku Solver

This module compares CSP techniques applied to Sudoku:

    Backtracking

    Minimum Remaining Values (MRV)

    Unit Propagation

    Backjumping

Running the Sudoku Benchmark

The project includes a dataset of 95 hard Sudoku puzzles (Sudoku_Dataset/sudoku95test.txt).

To solve the puzzles and compare the performance of the different algorithms, navigate to the Sudoku directory and run the main script:
Bash

cd Sudoku
python main.py

3. Bonus: Minesweeper Solver

This module uses a custom SAT solver (DPLL) to logically deduce safe squares in Minesweeper without guessing.

Running the Tests

There are two test suites available to verify the solver's logic against various board configurations. Navigate to the Bonus directory to run them.

Run the basic test suite:
Bash

cd Bonus
python testing-suite-1.py

Run the comprehensive test suite (includes corner cases and complex logic patterns):
Bash

cd Bonus
python testing-suite-2.py

Troubleshooting

    RecursionError: Some solvers (especially Naive or pure DPLL on large inputs) may hit the Python recursion limit. The scripts include sys.setrecursionlimit(), but if you experience a crash, try increasing this value in the respective .py file.

    FileNotFoundError: Ensure you are running the scripts from inside their respective directories (e.g., run main.py from inside Sudoku/, not from the root).
