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
