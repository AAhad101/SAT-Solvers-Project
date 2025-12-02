SAT & Constraint Satisfaction Project

This repository contains implementations of various Constraint Satisfaction Problem (CSP) and Boolean Satisfiability (SAT) solvers.
It includes solvers for:

SAT (DIMACS CNF)

Sudoku

Minesweeper (SAT-based inference bot)

All implementations rely only on Python's Standard Library
(multiprocessing, unittest, random, sys, os, copy, itertools).

📁 Project Structure
.
├── SAT/        → SAT solvers (Naive, Degree Heuristic, DPLL, CBJ)
├── Sudoku/     → Sudoku solvers with CSP heuristics
└── Bonus/      → Minesweeper solver using SAT logic inference

1. SAT Solvers

This module implements four algorithms to solve 3-SAT problems:

✔️ Naive Backtracking

✔️ Degree Heuristic

✔️ DPLL (Davis–Putnam–Logemann–Loveland) with Unit Propagation

✔️ Conflict-Directed Backjumping (CBJ)

📂 Dataset

Located in:

SAT/SAT_Dataset/


Includes:

Random 3-SAT instances

Pigeonhole Principle benchmarks

▶️ Running the SAT Benchmark
cd SAT
python sat_benchmark.py


The benchmark prints:

Solver name

Execution time

Result (SAT / UNSAT)

2. Sudoku Solver

This module compares multiple CSP strategies applied to Sudoku:

✔️ Naive Backtracking

✔️ Backtracking + MRV (Minimum Remaining Values)

✔️ Unit Propagation

✔️ Conflict-Directed Backjumping (CBJ)

📂 Dataset
Sudoku/Sudoku_Dataset/


Contains 95 hard Sudoku puzzles.

▶️ Running the Sudoku Benchmark
cd Sudoku
python main.py


The script solves all puzzles and compares performance across algorithms.

3. Bonus: Minesweeper Solver (SAT-Based)

This module uses a DPLL SAT solver to play Minesweeper without guessing.
It deduces:

✔️ Safe cells

✔️ Mine cells

based purely on logical inference.

▶️ Running Tests

1. Basic Test Suite

cd Bonus
python testing-suite-1.py


2. Comprehensive Test Suite
Tests advanced patterns (1-2-1, extended constraints, corners):

cd Bonus
python testing-suite-2.py

🛠 Troubleshooting
1. RecursionError

Some solvers (e.g., Naive Backtracking) may exceed Python's recursion limit.

Fix by increasing sys.setrecursionlimit():

sys.setrecursionlimit(10000)

2. FileNotFoundError

Scripts use relative paths, so run them from inside their respective folders:

❌ Wrong:

python SAT/sat_benchmark.py


✔️ Correct:

cd SAT
python sat_benchmark.py
