import copy

def solve_naive(clauses, num_vars):
    def simplify(current, var, val):
        new = []
        for clause in current:
            if (var in clause and val) or (-var in clause and not val):
                continue
            new_clause = [lit for lit in clause if abs(lit) != var]
            if not new_clause:
                return None
            new.append(new_clause)
        return new

    def backtrack(c, a):
        if not c:
            return a
        
        lit = c[0][0]
        var = abs(lit)

        for val in (True, False):
            nc = simplify(c, var, val)
            if nc is not None:
                r = backtrack(nc, {**a, var: val})
                if r:
                    return r
        return None

    return backtrack(clauses, {})
