import copy
from itertools import combinations


def solve_dpll(clauses, num_vars):

    def unit_propagate(formula, assignment):
        changed = True
        while changed:
            changed = False
            for clause in formula:
                unassigned = []
                satisfied = False

                # Scan clause
                for lit in clause:
                    var = abs(lit)
                    if var in assignment:
                        if (lit > 0 and assignment[var]) or (lit < 0 and not assignment[var]):
                            satisfied = True
                            break
                    else:
                        unassigned.append(lit)

                if satisfied:
                    continue

                # Clause fully false → conflict
                if len(unassigned) == 0:
                    return None, assignment, True

                # Unit clause → forced assignment
                if len(unassigned) == 1:
                    unit = unassigned[0]
                    var = abs(unit)
                    val = (unit > 0)

                    if var in assignment and assignment[var] != val:
                        return None, assignment, True

                    if var not in assignment:
                        assignment[var] = val
                        changed = True

        # Simplify formula
        new_formula = []
        for clause in formula:
            satisfied = False
            new_clause = []
            for lit in clause:
                var = abs(lit)
                if var in assignment:
                    if (lit > 0 and assignment[var]) or (lit < 0 and not assignment[var]):
                        satisfied = True
                        break
                else:
                    new_clause.append(lit)
            if not satisfied:
                new_formula.append(new_clause)

        return new_formula, assignment, False


    def dpll(formula, assignment):
        formula, assignment, conflict = unit_propagate(formula, assignment)
        if conflict:
            return None
        if not formula:
            return assignment  # SAT success!

        # Pick first literal in first remaining clause (naive)
        lit = formula[0][0]
        var = abs(lit)

        # Try True
        res = dpll(formula + [[var]], copy.copy(assignment))
        if res is not None:
            return res

        # Try False
        res = dpll(formula + [[-var]], copy.copy(assignment))
        if res is not None:
            return res

        return None

    return dpll(clauses, {})


def solve_sat(clauses):
    result = solve_dpll(clauses, 1000)
    return result is not None


def neighbors(r, c, rows, cols):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                yield (nr, nc)


def at_least(vars, t):
    clauses = []
    n = len(vars)
    k = n - t + 1
    for comb in combinations(vars, k):
        clauses.append(list(comb))
    return clauses

def at_most(vars, t):
    clauses = []
    for comb in combinations(vars, t+1):
        clauses.append([-v for v in comb])
    return clauses

def exactly(vars, t):
    if t < 0 or t > len(vars):
        return [[]]  # impossible ⇒ UNSAT
    return at_least(vars, t) + at_most(vars, t)


def encode_board(board):
    rows, cols = len(board), len(board[0])
    var_map = {}
    clauses = []
    next_var = 1

    # Assign variables to unknown cells
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == -1:  # unknown cell
                var_map[(r, c)] = next_var
                next_var += 1

    # Add number constraints
    for r in range(rows):
        for c in range(cols):
            if 8 >= board[r][c] >= 0:  # revealed number or confirmed safe
                number = board[r][c]
                hidden = []
                flagged = 0

                for nr, nc in neighbors(r, c, rows, cols):
                    if board[nr][nc] == -1:
                        hidden.append(var_map[(nr, nc)])
                    elif board[nr][nc] == 9:  # flagged mine
                        flagged += 1

                need = number - flagged
                clauses += exactly(hidden, need)

    return clauses, var_map


def infer_moves(board):
    clauses, var_map = encode_board(board)
    results = {}

    for (r, c), v in var_map.items():
        # Assume mine
        mine_sat = solve_sat(clauses + [[v]])
        # Assume safe
        safe_sat = solve_sat(clauses + [[-v]])

        if not mine_sat and safe_sat:
            results[(r, c)] = "SAFE"
        elif mine_sat and not safe_sat:
            results[(r, c)] = "MINE"
        else:
            results[(r, c)] = "UNKNOWN"

    return results


def apply_inference(board, solution_board, inference):
    """
    Updates the board:
      SAFE  -> reveal the cell using solution_board
      MINE  -> mark as 9 (flag)
      UNKNOWN -> keep as -1
    """
    new_board = [row[:] for row in board]
    
    for (r, c), status in inference.items():
        if status == "MINE":
            new_board[r][c] = 9  # mark mine
        elif status == "SAFE":
            # Reveal the cell from solution board
            if solution_board[r][c] == 9:
                print(f"ERROR: SAT solver marked mine at ({r},{c}) as SAFE!")
                new_board[r][c] = 9  # Should be a mine
            else:
                # Simply copy the value from solution board
                new_board[r][c] = solution_board[r][c]
    
    return new_board


def print_board(board):
    """Pretty print the board."""
    for row in board:
        print(row)


def is_fully_solved(board):
    """Returns True if there are no hidden cells (-1) remaining."""
    for row in board:
        if -1 in row:
            return False
    return True


def auto_solve(board, solution_board, max_iterations=50, debug=True):
    """
    Automatically solve minesweeper using SAT solver.
    
    Args:
        board: Current game board (-1 = unknown, 0-8 = revealed number, 9 = flagged mine)
        solution_board: Ground truth board (0-8 = safe cells, 9 = mines)
        max_iterations: Maximum solving iterations
        debug: Print debug information
    """
    iteration = 1

    while iteration <= max_iterations:
        if debug:
            print(f"\nSAT deduction iteration {iteration}")
            print_board(board)

        # Get new inference
        inference = infer_moves(board)

        # Apply inference to board
        updated_board = apply_inference(board, solution_board, inference)

        # Check if board changed
        changed = (updated_board != board)

        # Update board now
        board[:] = updated_board  # In-place copy

        if is_fully_solved(board):
            print("\nPuzzle fully solved by logical SAT deductions!")
            print_board(board)
            return True

        if not changed:
            if debug:
                print("\nNo further logical deductions possible.")
            break

        iteration += 1

    print("\nFinal logically deduced board:")
    print_board(board)
    print("SAT solver is stuck — guessing would be needed to continue.")
    return False


# Example usage:
# 0-8: number of mines around that cell (safe cell)
# 9: mine
# -1: unknown cell

# Solution board (ground truth)
solution_board = [
    [0, 0, 0, 0, 1, 9],
    [0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0],
    [9, 1, 0, 0, 0, 0]
]

# Initial unsolved board
unsolved_board = [
    [-1, -1, -1, -1, -1, -1],
    [-1, -1,  0,  0, -1, -1],
    [-1,  0,  0,  0,  0, -1],
    [-1,  0,  0,  0,  0, -1],
    [-1,  1,  0,  0,  0, -1],
    [-1, -1,  0,  0,  0, -1]
]

print("Solution Board (Ground Truth):")
print_board(solution_board)
print("\nStarting Board:")
print_board(unsolved_board)

auto_solve(unsolved_board, solution_board)