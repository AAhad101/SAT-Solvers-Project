import os
import random

def generate_random_3sat(filename, num_vars, num_clauses):
    """
    Generates a Random 3-SAT problem near the phase transition.
    Ratio ~4.26 is the 'hardest' region for SAT solvers.
    """
    with open(filename, 'w') as f:
        f.write(f"c Random 3-SAT generated for Python Benchmarking\n")
        f.write(f"p cnf {num_vars} {num_clauses}\n")
        
        used_clauses = set()
        
        while len(used_clauses) < num_clauses:
            # Pick 3 distinct variables
            vars = random.sample(range(1, num_vars + 1), 3)
            # Randomly negate them
            literals = [v * random.choice([1, -1]) for v in vars]
            
            # Create immutable tuple for set storage
            clause_tuple = tuple(sorted(literals, key=abs))
            
            if clause_tuple not in used_clauses:
                used_clauses.add(clause_tuple)
                f.write(f"{literals[0]} {literals[1]} {literals[2]} 0\n")

def generate_pigeonhole(filename, pigeons, holes):
    """
    Generates a Pigeonhole Principle problem (P pigeons into H holes).
    If P > H, this is UNSATISFIABLE, but hard to prove.
    """
    num_vars = pigeons * holes
    
    # Helper to get var index (1-based)
    def get_var(p, h): # p=1..P, h=1..H
        return (p - 1) * holes + h

    clauses = []

    # 1. Each pigeon must be in at least one hole
    for p in range(1, pigeons + 1):
        clause = []
        for h in range(1, holes + 1):
            clause.append(get_var(p, h))
        clauses.append(clause)

    # 2. No hole can have two pigeons (Conflict)
    for h in range(1, holes + 1):
        for p1 in range(1, pigeons + 1):
            for p2 in range(p1 + 1, pigeons + 1):
                # Not (p1 in h AND p2 in h)  ==  (Not p1 in h OR Not p2 in h)
                clauses.append([-get_var(p1, h), -get_var(p2, h)])

    with open(filename, 'w') as f:
        f.write(f"c Pigeonhole Principle {pigeons} pigeons in {holes} holes\n")
        f.write(f"p cnf {num_vars} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")

def main():
    output_dir = "SAT_Dataset"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"Generating 20 benchmark files in '{output_dir}'...")

    # --- Set 1: Random 3-SAT (N=30) [EASY] ---
    # Ratio 4.26 -> ~128 clauses
    for i in range(1, 6):
        generate_random_3sat(f"{output_dir}/rnd_n30_0{i}.cnf", 30, 128)

    # --- Set 2: Random 3-SAT (N=50) [MEDIUM] ---
    # Ratio 4.26 -> ~213 clauses
    for i in range(1, 6):
        generate_random_3sat(f"{output_dir}/rnd_n50_0{i}.cnf", 50, 213)

    # --- Set 3: Random 3-SAT (N=75) [HARD] ---
    # Ratio 4.26 -> ~320 clauses
    # These might still timeout Naive, but DPLL should sweat
    for i in range(1, 6):
        generate_random_3sat(f"{output_dir}/rnd_n75_0{i}.cnf", 75, 320)

    # --- Set 4: Pigeonhole Principle (Logic Test) ---
    # PHP 4-3 (12 vars) - Easy
    generate_pigeonhole(f"{output_dir}/php_4_3.cnf", 4, 3)
    # PHP 5-4 (20 vars) - Medium
    generate_pigeonhole(f"{output_dir}/php_5_4.cnf", 5, 4)
    # PHP 6-5 (30 vars) - Hard (Exponentially harder for resolution)
    generate_pigeonhole(f"{output_dir}/php_6_5.cnf", 6, 5)
    # PHP 7-6 (42 vars) - Very Hard
    generate_pigeonhole(f"{output_dir}/php_7_6.cnf", 7, 6)
    # PHP 8-7 (56 vars) - Extreme
    generate_pigeonhole(f"{output_dir}/php_8_7.cnf", 8, 7)

    print("Done! You can now run the benchmark script.")

if __name__ == "__main__":
    main()
