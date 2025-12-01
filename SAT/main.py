import os, glob, time, multiprocessing
from parsing import parse_dimacs_cnf, verify_solution
from naive import solve_naive
from degree_heuristic import solve_degree_heuristic
from dpll import solve_dpll
from backjumping import solve_backjumping

def worker(solver, clauses, n, ret):
    try:
        start = time.time()
        sol = solver(clauses, n)
        ret['time'] = time.time() - start
        ret['result'] = sol
    except Exception as e:
        ret['error'] = str(e)

def run_benchmark():
    TIMEOUT = 30
    files = sorted(glob.glob("SAT_Dataset/*.cnf"))
    solvers = {
        "Naive": solve_naive,
        "Degree": solve_degree_heuristic,
        "DPLL": solve_dpll,
        "Backjump": solve_backjumping
    }

    for f in files:
        print(f"\nFile: {os.path.basename(f)}")
        clauses, n = parse_dimacs_cnf(f)
        print(f"Vars: {n}, Clauses: {len(clauses)}")

        for name, solver in solvers.items():
            manager = multiprocessing.Manager()
            ret = manager.dict()
            p = multiprocessing.Process(target=worker, args=(solver, clauses, n, ret))
            p.start()
            p.join(TIMEOUT)

            if p.is_alive():
                p.terminate()
                print(f"  {name}: TIMEOUT")
            elif 'error' in ret:
                print(f"  {name}: ERROR {ret['error']}")
            else:
                t = ret['time']
                res = ret['result']
                status = "SAT" if res else "UNSAT"
                valid = verify_solution(clauses, res) if res else True
                print(f"  {name}: {status} in {t:.4f}s [{ 'Valid' if valid else 'INVALID'} ]")

if __name__ == "__main__":
    run_benchmark()
