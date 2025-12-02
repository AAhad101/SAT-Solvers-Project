# SAT & Constraint Satisfaction Project

This repository contains implementations of various **Constraint
Satisfaction Problem (CSP)** and **Boolean Satisfiability (SAT)**
solvers. It includes:

-   SAT (DIMACS CNF)
-   Sudoku
-   Minesweeper (SAT-based inference bot)

All implementations rely **only on Python's Standard Library**.

## Project Structure

    .
    ├── SAT/        → SAT solvers (Naive, Degree Heuristic, DPLL, CBJ)
    ├── Sudoku/     → Sudoku solvers with CSP heuristics
    └── Bonus/      → Minesweeper solver using SAT logic inference

# 1. SAT Solvers

Implements:

-   Naive Backtracking
-   Degree Heuristic
-   DPLL with Unit Propagation
-   Conflict-Directed Backjumping (CBJ)

### Dataset

Located in `SAT/SAT_Dataset/`.

### Running Benchmark

``` bash
cd SAT
python sat_benchmark.py
```

# 2. Sudoku Solver

Strategies:

-   Naive Backtracking
-   MRV
-   Unit Propagation
-   CBJ

### Dataset

`Sudoku/Sudoku_Dataset/`

### Run:

``` bash
cd Sudoku
python main.py
```

# 3. Minesweeper SAT Solver

Uses DPLL to infer safe/mine cells logically.

### Tests

``` bash
cd Bonus
python testing-suite-1.py
python testing-suite-2.py
```

# Troubleshooting

### RecursionError

Increase:

``` python
sys.setrecursionlimit(10000)
```

### FileNotFoundError

Use correct directory:

``` bash
cd SAT
python sat_benchmark.py
```
