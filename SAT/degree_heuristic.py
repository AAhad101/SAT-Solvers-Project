def solve_degree_heuristic(clauses, num_vars):

    def consistent(a):
        for clause in clauses:
            clause_val = False
            all_assigned = True
            for lit in clause:
                if abs(lit) not in a:
                    all_assigned = False
                else:
                    v = a[abs(lit)]
                    if (lit > 0 and v) or (lit < 0 and not v):
                        clause_val = True
                        break
            if all_assigned and not clause_val:
                return False
        return True

    def choose_var(vars, a):
        best = None
        best_score = -1
        for v in vars:
            score = sum(
                not any(
                    abs(l) in a and 
                    ((l > 0 and a[abs(l)]) or (l < 0 and not a[abs(l)]))
                    for l in c
                )
                for c in clauses if v in [abs(l) for l in c]
            )
            if score > best_score:
                best = v
                best_score = score
        return best

    def backtrack(a, vars):
        if not vars:
            return a if consistent(a) else None
        var = choose_var(vars, a)
        for val in (True, False):
            a[var] = val
            if consistent(a):
                result = backtrack(a, vars - {var})
                if result:
                    return result
            del a[var]
        return None

    return backtrack({}, set(range(1, num_vars + 1)))
