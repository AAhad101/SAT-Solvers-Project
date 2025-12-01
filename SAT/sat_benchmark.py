import os
import time
import sys
import copy
import glob
import multiprocessing
from typing import List, Dict, Optional, Tuple, Set

# Increase recursion depth for deep search trees
sys.setrecursionlimit(10000)

# ==========================================
# 1. PARSING & VERIFICATION UTILITIES
# ==========================================

def parse_dimacs_cnf(filepath: str) -> Tuple[List[List[int]], int]:
    """Parses .cnf files."""
    clauses = []
    num_vars = 0
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('c') or line.startswith('%') or line.startswith('0'):
                    continue
                if line.startswith('p'):
                    try:
                        parts = line.split()
                        num_vars = int(parts[2])
                    except: pass
                    continue
                try:
                    parts = [int(x) for x in line.split()]
                    if parts and parts[-1] == 0: parts.pop()
                    if parts: clauses.append(parts)
                except ValueError: continue
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return [], 0
    
    if clauses:
        # Recalculate max var to be safe
        real_max = max(abs(l) for c in clauses for l in c)
        num_vars = max(num_vars, real_max)
    return clauses, num_vars

def verify_solution(clauses: List[List[int]], assignment: Dict[int, bool]) -> bool:
    """Verifies if the given assignment satisfies all clauses."""
    if assignment is None: return False
    for c in clauses:
        satisfied = False
        for lit in c:
            val = assignment.get(abs(lit))
            # Lit is true if (val is True and lit > 0) OR (val is False and lit < 0)
            if (lit > 0 and val is True) or (lit < 0 and val is False):
                satisfied = True
                break
        if not satisfied:
            return False
    return True

# ==========================================
# 2. SOLVER IMPLEMENTATIONS
# ==========================================

# --- Solver 1: Naive Backtracking ---
def solve_naive(clauses, num_vars):
    # Helper to simplify clauses based on assignment
    def simplify(current_clauses, var, val):
        new_clauses = []
        for clause in current_clauses:
            # If satisfied, remove it
            if (var in clause and val) or (-var in clause and not val):
                continue 
            # If false literal, remove literal from clause
            new_clause = [lit for lit in clause if abs(lit) != var]
            if not new_clause: return None # Empty clause = Conflict
            new_clauses.append(new_clause)
        return new_clauses

    def backtrack(current_clauses, assignment):
        if not current_clauses: return assignment
        
        # Heuristic: Pick first literal of first clause
        lit = current_clauses[0][0]
        var = abs(lit)
        
        # Try True
        new_c = simplify(current_clauses, var, True)
        if new_c is not None:
            res = backtrack(new_c, {**assignment, var: True})
            if res is not None: return res
            
        # Try False
        new_c = simplify(current_clauses, var, False)
        if new_c is not None:
            res = backtrack(new_c, {**assignment, var: False})
            if res is not None: return res
            
        return None

    return backtrack(clauses, {})


# --- Solver 2: Degree Heuristic ---
def solve_degree_heuristic(clauses, num_vars):
    
    def is_consistent(assignment, clauses):
        for clause in clauses:
            clause_val = False
            all_assigned = True
            for lit in clause:
                if abs(lit) in assignment:
                    val = assignment[abs(lit)]
                    if (lit > 0 and val) or (lit < 0 and not val):
                        clause_val = True
                        break
                else:
                    all_assigned = False
            if all_assigned and not clause_val:
                return False
        return True

    def select_most_constrained_var(variables, assignment, clauses):
        best_var = None
        max_constraints = -1
        
        # Pick var in most currently-unsatisfied clauses
        for var in variables:
            count = 0
            for clause in clauses:
                if var in [abs(x) for x in clause]:
                    is_satisfied = False
                    for lit in clause:
                        if abs(lit) in assignment:
                            v = assignment[abs(lit)]
                            if (lit > 0 and v) or (lit < 0 and not v):
                                is_satisfied = True
                                break
                    if not is_satisfied:
                        count += 1
            if count > max_constraints:
                max_constraints = count
                best_var = var
        return best_var if best_var else list(variables)[0]

    def backtrack(assignment, variables):
        if not variables:
            return assignment if is_consistent(assignment, clauses) else None
        
        var = select_most_constrained_var(variables, assignment, clauses)
        
        for val in [True, False]:
            assignment[var] = val
            if is_consistent(assignment, clauses):
                res = backtrack(assignment, variables - {var})
                if res: return res
            del assignment[var]
        return None

    all_vars = set(range(1, num_vars + 1))
    return backtrack({}, all_vars)


# --- Solver 3: DPLL (Unit Propagation) ---
def solve_dpll(clauses, num_vars):
    
    def unit_propagate(formula, assignment):
        process = True
        while process:
            process = False
            units = []
            for clause in formula:
                unassigned = []
                sat = False
                for lit in clause:
                    if abs(lit) in assignment:
                        val = assignment[abs(lit)]
                        if (lit > 0 and val) or (lit < 0 and not val):
                            sat = True; break
                    else:
                        unassigned.append(lit)
                if sat: continue
                if not unassigned: return None, None, True # Conflict
                if len(unassigned) == 1: units.append(unassigned[0])
            
            for lit in set(units):
                var = abs(lit)
                val = (lit > 0)
                if var in assignment and assignment[var] != val: return None, None, True
                if var not in assignment:
                    assignment[var] = val
                    process = True
        
        # Simplify
        simplified = []
        for clause in formula:
            sat = False
            new_c = []
            for lit in clause:
                if abs(lit) in assignment:
                    val = assignment[abs(lit)]
                    if (lit > 0 and val) or (lit < 0 and not val): sat = True; break
                else: new_c.append(lit)
            if not sat:
                simplified.append(new_c)
        return simplified, assignment, False

    def backtrack(formula, assignment):
        formula, assignment, conflict = unit_propagate(formula, assignment)
        if conflict: return None
        if not formula: return assignment
        
        # Heuristic: First literal of first clause
        lit = formula[0][0]
        var = abs(lit)
        
        # Branch True
        res = backtrack(formula + [[var]], copy.copy(assignment))
        if res: return res
        
        # Branch False
        res = backtrack(formula + [[-var]], copy.copy(assignment))
        if res: return res
        
        return None

    return backtrack(clauses, {})


# --- Solver 4: Backjumping (CBJ) ---
class CBJSolver:
    def __init__(self, clauses, num_vars):
        self.clauses = clauses
        self.num_vars = num_vars
        self.assignment: Dict[int, bool] = {}
        self.solution: Optional[Dict[int, bool]] = None
        self.conflict_sets: Dict[int, Set[int]] = {}

    def pick_unassigned(self) -> Optional[int]:
        for v in range(1, self.num_vars + 1):
            if v not in self.assignment:
                return v
        return None

    def clause_state(self, clause: List[int]) -> str:
        has_unassigned = False
        for lit in clause:
            val = self.assignment.get(abs(lit))
            if val is None:
                has_unassigned = True
                continue
            if (lit > 0 and val) or (lit < 0 and not val):
                return "SAT"
        return "UNRESOLVED" if has_unassigned else "CONFLICT"

    def find_conflict_clause(self) -> Optional[List[int]]:
        for clause in self.clauses:
            if self.clause_state(clause) == "CONFLICT":
                return clause
        return None

    def all_clauses_satisfied(self) -> bool:
        for clause in self.clauses:
            if self.clause_state(clause) != "SAT":
                return False
        return True

    def search(self) -> Tuple[bool, Set[int]]:
        conflict_clause = self.find_conflict_clause()
        if conflict_clause is not None:
            return False, {abs(l) for l in conflict_clause}

        if self.all_clauses_satisfied():
            self.solution = dict(self.assignment)
            return True, set()

        var = self.pick_unassigned()
        if var is None:
            self.solution = dict(self.assignment)
            return True, set()

        self.conflict_sets[var] = set()
        for val in (True, False):
            self.assignment[var] = val
            sat, conflict = self.search()
            if sat:
                return True, set()
            conflict = set(conflict)
            if var not in conflict:
                del self.assignment[var]
                self.conflict_sets[var].update(conflict)
                return False, conflict
            conflict.discard(var)
            self.conflict_sets[var].update(conflict)
            del self.assignment[var]

        conflict = set(self.conflict_sets[var])
        conflict.add(var)
        return False, conflict

    def solve(self):
        result, _ = self.search()
        return result

def solve_backjumping(clauses, num_vars):
    solver = CBJSolver(clauses, num_vars)
    if solver.solve():
        return solver.solution
    return None


# ==========================================
# 3. BENCHMARK HARNESS (MULTIPROCESSING)
# ==========================================

def worker(solver_name, clauses, num_vars, return_dict):
    """Run solver in isolated process."""
    try:
        start = time.time()
        if solver_name == "Naive":
            res = solve_naive(clauses, num_vars)
        elif solver_name == "Degree Heuristic":
            res = solve_degree_heuristic(clauses, num_vars)
        elif solver_name == "DPLL":
            res = solve_dpll(clauses, num_vars)
        elif solver_name == "Backjumping":
            res = solve_backjumping(clauses, num_vars)
        else:
            res = None
            
        return_dict['time'] = time.time() - start
        return_dict['result'] = res
    except RecursionError:
        return_dict['error'] = "Recursion Limit"
    except Exception as e:
        return_dict['error'] = str(e)

def run_benchmark():
    TIMEOUT = 30 # Seconds per solver
    input_dir = "SAT_Dataset"
    
    files = sorted(glob.glob(os.path.join(input_dir, "*.cnf")))
    if not files:
        print(f"No files found in '{input_dir}'. Please run generate_tests.py first!")
        return

    print(f"Benchmarking {len(files)} files in '{input_dir}' with {TIMEOUT}s timeout.")
    print("-" * 60)
    
    solvers = ["Naive", "Degree Heuristic", "DPLL", "Backjumping"]
    
    for filepath in files:
        filename = os.path.basename(filepath)
        print(f"\nFile: {filename}")
        clauses, n_vars = parse_dimacs_cnf(filepath)
        print(f"Vars: {n_vars}, Clauses: {len(clauses)}")

        for name in solvers:
            manager = multiprocessing.Manager()
            ret = manager.dict()
            
            # Spawn process
            p = multiprocessing.Process(target=worker, args=(name, clauses, n_vars, ret))
            p.start()
            p.join(TIMEOUT)
            
            if p.is_alive():
                p.terminate()
                p.join()
                print(f"  {name:<12}: TIMEOUT")
            elif 'error' in ret:
                print(f"  {name:<12}: ERROR ({ret['error']})")
            else:
                t = ret['time']
                res = ret['result']
                status = "SAT" if res else "UNSAT"
                
                # Verify validity if SAT
                check = ""
                if res:
                    if verify_solution(clauses, res):
                        check = "[Valid]"
                    else:
                        check = "[INVALID]"
                        status = "ERROR"
                
                print(f"  {name:<12}: {status:<5} in {t:.4f}s {check}")

if __name__ == "__main__":
    run_benchmark()
