import sys
from typing import List, Dict, Tuple

sys.setrecursionlimit(10000)

def parse_dimacs_cnf(filepath: str) -> Tuple[List[List[int]], int]:
    clauses = []
    num_vars = 0
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('c') or line.startswith('%') or line.startswith('0'):
                    continue
                if line.startswith('p'):
                    parts = line.split()
                    try:
                        num_vars = int(parts[2])
                    except:
                        pass
                    continue
                try:
                    parts = [int(x) for x in line.split()]
                    if parts and parts[-1] == 0: parts.pop()
                    if parts:
                        clauses.append(parts)
                except ValueError:
                    continue
    except Exception as e:
        print(f"Error: {e}")
        return [], 0
    
    real_max = max(abs(l) for c in clauses for l in c) if clauses else 0
    return clauses, max(num_vars, real_max)

def verify_solution(clauses: List[List[int]], assignment: Dict[int, bool]) -> bool:
    if assignment is None:
        return False
    for clause in clauses:
        if not any(
            (lit > 0 and assignment.get(abs(lit)) is True) or
            (lit < 0 and assignment.get(abs(lit)) is False)
            for lit in clause
        ):
            return False
    return True
