import time
import copy
import sys

# Increase recursion depth just in case
sys.setrecursionlimit(5000)

# ==========================================
# 1. PARSING UTILITIES
# ==========================================

def parse_sudoku_file(filepath):
    """
    Parses the sudoku95test.txt or soln_raw.txt format.
    """
    boards = []
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
        # Normalize whitespace and split
        # Replace dots with 0 for easier integer conversion
        tokens = content.replace('.', '0').split()
        
        current_values = []
        
        for token in tokens:
            # Skip source tags like 
            if token.startswith('[') or token.endswith(']'):
                continue
            
            if token.isdigit():
                current_values.append(int(token))
                
                # If we have 81 numbers, that's a full board
                if len(current_values) == 81:
                    # Convert 1D list of 81 ints to 9x9 2D list
                    board_2d = [current_values[i:i+9] for i in range(0, 81, 9)]
                    boards.append(board_2d)
                    current_values = []
                    
        return boards
    except FileNotFoundError:
        print(f"Error: Could not find file {filepath}")
        return []

def boards_match(b1, b2):
    """Compares two 9x9 boards for equality."""
    if not b1 or not b2:
        return False
    for r in range(9):
        for c in range(9):
            if b1[r][c] != b2[r][c]:
                return False
    return True

# ==========================================
# 2. SOLVER ALGORITHMS
# ==========================================

# --- Algorithm 1: Naive Backtracking ---
def solve_backtracking(board):
    def is_valid(b, r, c, num):
        for i in range(9):
            if b[r][i] == num or b[i][c] == num: return False
        br, bc = (r // 3) * 3, (c // 3) * 3
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if b[i][j] == num: return False
        return True

    def find_empty(b):
        for r in range(9):
            for c in range(9):
                if b[r][c] == 0: return r, c
        return None

    empty = find_empty(board)
    if not empty: return True
    r, c = empty
    
    for num in range(1, 10):
        if is_valid(board, r, c, num):
            board[r][c] = num
            if solve_backtracking(board): return True
            board[r][c] = 0
    return False

# --- Algorithm 2: MRV Backtracking ---
def solve_mrv(board):
    def get_valid_values(b, r, c):
        valid = set(range(1, 10))
        valid -= set(b[r])
        valid -= {b[i][c] for i in range(9)}
        br, bc = (r // 3) * 3, (c // 3) * 3
        valid -= {b[i][j] for i in range(br, br + 3) for j in range(bc, bc + 3)}
        return valid

    def select_mrv_cell(b):
        min_len = 10
        best_cell = None
        for r in range(9):
            for c in range(9):
                if b[r][c] == 0:
                    possibles = get_valid_values(b, r, c)
                    if len(possibles) == 0: return (r, c), [] # Dead end
                    if len(possibles) < min_len:
                        min_len = len(possibles)
                        best_cell = (r, c)
                        best_vals = possibles
        if best_cell: return best_cell, best_vals
        return None, None

    cell, values = select_mrv_cell(board)
    if cell is None: return True # Solved
    if not values: return False # Dead end found by MRV check
    
    r, c = cell
    for val in values:
        board[r][c] = val
        if solve_mrv(board): return True
        board[r][c] = 0
    return False

# --- Algorithm 3: Unit Propagation ---
def solve_unit_prop(board):
    # Helper to set up domains
    def init_domains(b):
        domains = {}
        for r in range(9):
            for c in range(9):
                if b[r][c] == 0: domains[(r, c)] = set(range(1, 10))
                else: domains[(r, c)] = {b[r][c]}
        return domains

    def peers(r, c):
        p = set()
        for i in range(9):
            if i != c: p.add((r, i))
            if i != r: p.add((i, c))
        br, bc = (r//3)*3, (c//3)*3
        for i in range(br, br+3):
            for j in range(bc, bc+3):
                if (i, j) != (r, c): p.add((i, j))
        return p

    def propagate(domains):
        changed = True
        while changed:
            changed = False
            for cell, vals in list(domains.items()):
                if len(vals) == 1:
                    val = next(iter(vals))
                    for p in peers(*cell):
                        if val in domains[p]:
                            domains[p].remove(val)
                            if not domains[p]: return False # Conflict
                            changed = True
        return True

    def search(domains):
        if not propagate(domains): return None
        if all(len(v) == 1 for v in domains.values()): return domains
        
        # MRV choice within Unit Prop
        unassigned = {k: v for k, v in domains.items() if len(v) > 1}
        if not unassigned: return domains
        var = min(unassigned, key=lambda k: len(domains[k]))
        
        for val in unassigned[var]:
            new_domains = copy.deepcopy(domains)
            new_domains[var] = {val}
            res = search(new_domains)
            if res: return res
        return None

    domains = init_domains(board)
    result_domains = search(domains)
    
    if result_domains:
        # Fill board with result
        for (r, c), vals in result_domains.items():
            board[r][c] = next(iter(vals))
        return True
    return False

# --- Algorithm 4: Optimized Backjumping (CBJ) ---
def solve_backjumping(board):
    """
    An optimized implementation of Conflict-Directed Backjumping.
    Uses pre-computed peer indices to minimize overhead.
    """
    # 1. Precompute Empty Cells and Mappings
    cells = []
    cell_indices = {}
    idx_counter = 0
    
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                cells.append((r, c))
                cell_indices[(r, c)] = idx_counter
                idx_counter += 1
    
    if not cells:
        return True

    # 2. Precompute Peers for every empty cell
    # 'variable_peers' contains indices of other empty cells that conflict
    # 'fixed_peers' contains (r,c) of pre-filled cells that conflict
    variable_peers = {i: [] for i in range(len(cells))}
    fixed_peers = {i: [] for i in range(len(cells))}
    
    for i, (r, c) in enumerate(cells):
        # Find all neighbors (row, col, box)
        neighbors = set()
        for k in range(9):
            neighbors.add((r, k)) # Row
            neighbors.add((k, c)) # Col
        br, bc = (r // 3) * 3, (c // 3) * 3
        for brr in range(br, br+3):
            for bcc in range(bc, bc+3):
                neighbors.add((brr, bcc))
        
        neighbors.discard((r, c))
        
        for (nr, nc) in neighbors:
            if (nr, nc) in cell_indices:
                variable_peers[i].append(cell_indices[(nr, nc)])
            elif board[nr][nc] != 0:
                fixed_peers[i].append((nr, nc))

    # 3. Recursive Solver
    def solve(idx, conflict_sets):
        if idx == len(cells):
            return True
        
        r, c = cells[idx]
        
        # Initialize conflicts for this level
        current_conflicts = set()
        conflict_sets[idx] = current_conflicts
        
        my_fixed_peers = fixed_peers[idx]
        my_var_peers = variable_peers[idx]
        
        for val in range(1, 10):
            # --- Conflict Check ---
            is_conflict = False
            local_conflicts = set()
            
            # Check against fixed numbers
            for fr, fc in my_fixed_peers:
                if board[fr][fc] == val:
                    is_conflict = True
                    break # optimization: don't need to check others
            
            if is_conflict:
                continue # Try next value
                
            # Check against assigned variables (ancestors)
            for neighbor_idx in my_var_peers:
                # We only care about neighbors that are already assigned (index < current idx)
                if neighbor_idx < idx:
                    nr, nc = cells[neighbor_idx]
                    if board[nr][nc] == val:
                        is_conflict = True
                        local_conflicts.add(neighbor_idx)
            
            if is_conflict:
                current_conflicts.update(local_conflicts)
                continue

            # --- Valid Assignment ---
            board[r][c] = val
            
            res = solve(idx + 1, conflict_sets)
            
            if res is True:
                return True
            
            # --- Backtrack ---
            board[r][c] = 0
            
            # Handle Backjump
            # If res is an int, it is the target index we must jump to.
            if isinstance(res, int):
                if res == idx:
                    # We are the target. The child's conflicts have been merged into ours.
                    # Stop jumping and try the next value for THIS cell.
                    continue
                else:
                    # We are not the target. Pass the signal up.
                    return res
            
            # If res is None (standard backtrack?), it shouldn't happen with this logic
            # unless we decide to support standard backtracking fallbacks.
            
        # --- All values failed ---
        
        # If we have no variable conflicts (only fixed conflicts or empty), 
        # we must return None (Standard Backtrack) to parent.
        if not current_conflicts:
            return None
            
        # Jump to the most recent conflicting ancestor
        jump_target = max(current_conflicts)
        
        # Merge our conflicts into the target's conflict set
        if jump_target in conflict_sets:
            conflict_sets[jump_target].update(current_conflicts)
            conflict_sets[jump_target].discard(jump_target)
            
        return jump_target

    # Start Solving
    global_conflict_sets = {}
    result = solve(0, global_conflict_sets)
    return result is True


# ==========================================
# 3. BENCHMARK RUNNER
# ==========================================

def run_benchmark():
    test_file = "Sudoku_Dataset/sudoku95test.txt"
    soln_file = "Sudoku_Dataset/soln_raw.txt"
    output_file = "benchmark_results.txt"
    
    print(f"Loading puzzles from {test_file}...")
    puzzles = parse_sudoku_file(test_file)
    solutions = parse_sudoku_file(soln_file)
    
    if len(puzzles) != len(solutions):
        print(f"Error: Mismatch in counts. Puzzles: {len(puzzles)}, Solutions: {len(solutions)}")
        return

    print(f"Loaded {len(puzzles)} puzzles. Starting benchmark...\n")
    
    solvers = [
        ("Naive Backtracking", solve_backtracking),
        ("Backtracking + MRV", solve_mrv),
        ("Unit Propagation", solve_unit_prop),
        ("Backjumping (CBJ)", solve_backjumping)
    ]
    
    results = []
    
    for name, solver_func in solvers:
        print(f"Running {name}...")
        
        start_time = time.time()
        correct_count = 0
        
        # Copy puzzles to avoid modification between solvers
        current_puzzles = copy.deepcopy(puzzles)
        
        for i, puzzle in enumerate(current_puzzles):
            # Run solver
            try:
                solver_func(puzzle)
            except Exception as e:
                print(f"  Error on puzzle {i+1}: {e}")
            
            # Verify
            if boards_match(puzzle, solutions[i]):
                correct_count += 1
            else:
                print(f"  Mismatch on puzzle {i+1}")
        
        total_time = time.time() - start_time
        avg_time = total_time / len(puzzles) if len(puzzles) > 0 else 0
        
        print(f"  Done. Correct: {correct_count}/{len(puzzles)}. Time: {total_time:.4f}s")
        results.append(f"{name}\n  Correct: {correct_count}/{len(puzzles)}\n  Total Time: {total_time:.4f}s\n  Avg Time: {avg_time:.5f}s\n")

    # Save results
    with open(output_file, "w") as f:
        f.write("SUDOKU SOLVER BENCHMARK RESULTS\n")
        f.write("===============================\n\n")
        for r in results:
            f.write(r + "\n")
            
    print(f"\nBenchmark complete. Results saved to {output_file}")

if __name__ == "__main__":
    run_benchmark()
