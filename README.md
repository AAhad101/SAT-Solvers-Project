SAT & Constraint Satisfaction Project

This project implements various Constraint Satisfaction Problem (CSP) and Boolean Satisfiability (SAT) solvers. It includes implementations for solving SAT problems (CNF format), Sudoku puzzles, and a Minesweeper bot using logic inference.

Project Structure

The project is divided into three main modules:

    SAT/: Core SAT solvers for DIMACS CNF files.

    Sudoku/: Sudoku solvers comparing different heuristics.

    Bonus/: A Minesweeper solver using a SAT-based approach (DPLL).

Prerequisites

    Python 3.10 or higher.

    No external packages (pip install) are required. This project uses the Python Standard Library (multiprocessing, unittest, random, sys, os, copy).

1. SAT Solvers

This module implements four different algorithms to solve 3-SAT problems:

    Naive Backtracking

    Degree Heuristic

    DPLL (Davis–Putnam–Logemann–Loveland) with Unit Propagation

    Conflict-Directed Backjumping (CBJ)

Setup & Data Generation

Before running the benchmarks, you need to generate the test datasets (CNF files).

    Navigate to the SAT directory:
    Bash

cd SAT

Run the test generator. This will create a SAT_Dataset/ folder and populate it with Random 3-SAT problems and Pigeonhole Principle problems:
Bash

    python generate_tests.py

Running the SAT Benchmark

To run the solvers against the generated dataset using multiprocessing:
Bash

python sat_benchmark.py

Note: This script will run all four solvers against the .cnf files in SAT_Dataset and output the execution time and validity of the solution.

2. Sudoku Solver

This module compares CSP techniques applied to Sudoku:

    Backtracking

    Minimum Remaining Values (MRV)

    Unit Propagation

    Backjumping

Running the Sudoku Benchmark

The project includes a dataset of 95 hard Sudoku puzzles (sudoku95test.txt).

    Navigate to the Sudoku directory:
    Bash

cd Sudoku

Run the benchmark script:
Bash

    python main.py

    Alternatively, you can run python sudoku_benchmark.py if available.

This will attempt to solve the puzzles in Sudoku_Dataset/ and compare the performance of the different algorithms.

3. Bonus: Minesweeper Solver

This module uses a custom SAT solver (DPLL) to logically deduce safe squares in Minesweeper without guessing.

Running the Tests

There are two test suites available to verify the solver's logic against various board configurations.

    Navigate to the Bonus directory:
    Bash

cd Bonus

Run the basic test suite:
Bash

python testing-suite-1.py

Run the comprehensive test suite (includes corner cases and complex logic patterns):
Bash

    python testing-suite-2.py

Troubleshooting

    RecursionError: Some solvers (especially Naive or pure DPLL on large inputs) may hit the Python recursion limit. The scripts include sys.setrecursionlimit(), but if you crash, try increasing this value in the respective .py file.

    FileNotFoundError: Ensure you are running the scripts from inside their respective directories (e.g., run main.py from inside SAT/, not from the root), or ensure the *_Dataset folders exist.
