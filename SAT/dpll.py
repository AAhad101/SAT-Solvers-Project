import copy

def solve_dpll(clauses, num_vars):

    def unit_propagate(formula, a):
        changed = True
        while changed:
            changed = False
            units = []
            for clause in formula:
                unassigned = []
                satisfied = False
                for lit in clause:
                    if abs(lit) in a:
                        v = a[abs(lit)]
                        if (lit > 0 and v) or (lit < 0 and not v):
                            satisfied = True
                            break
                    else:
                        unassigned.append(lit)
                if satisfied:
                    continue
                if not unassigned:
                    return None, None, True
                if len(unassigned) == 1:
                    units.append(unassigned[0])
            for lit in set(units):
                v = abs(lit)
                val = lit > 0
                if v in a and a[v] != val:
                    return None, None, True
                if v not in a:
                    a[v] = val
                    changed = True

        new_f = []
        for clause in formula:
            if any(abs(l) in a and ((l > 0 and a[abs(l)]) or (l < 0 and not a[abs(l)])) for l in clause):
                continue
            new_clause = [l for l in clause if abs(l) not in a]
            new_f.append(new_clause)
        return new_f, a, False

    def backtrack(formula, a):
        formula, a, conflict = unit_propagate(formula, a)
        if conflict:
            return None
        if not formula:
            return a
        lit = formula[0][0]
        var = abs(lit)
        for val in (True, False):
            r = backtrack(formula + [[var if val else -var]], copy.copy(a))
            if r:
                return r
        return None

    return backtrack(clauses, {})
