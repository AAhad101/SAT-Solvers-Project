class CBJSolver:
    def __init__(self, clauses, num_vars):
        self.clauses = clauses
        self.num_vars = num_vars
        self.assignment = {}
        self.solution = None
        self.conflict_sets = {}

    def pick_unassigned(self):
        return next((v for v in range(1, self.num_vars + 1) if v not in self.assignment), None)

    def clause_state(self, clause):
        has_unassigned = False
        for lit in clause:
            val = self.assignment.get(abs(lit))
            if val is None:
                has_unassigned = True
            elif (lit > 0 and val) or (lit < 0 and not val):
                return "SAT"
        return "UNRESOLVED" if has_unassigned else "CONFLICT"

    def find_conflict(self):
        for c in self.clauses:
            if self.clause_state(c) == "CONFLICT":
                return c
        return None

    def all_satisfied(self):
        return all(self.clause_state(c) == "SAT" for c in self.clauses)

    def search(self):
        c = self.find_conflict()
        if c:
            return False, {abs(l) for l in c}

        if self.all_satisfied():
            self.solution = self.assignment.copy()
            return True, set()

        v = self.pick_unassigned()
        self.conflict_sets[v] = set()
        for val in (True, False):
            self.assignment[v] = val
            sat, conf = self.search()
            if sat:
                return True, set()
            conf = set(conf)
            if v not in conf:
                del self.assignment[v]
                self.conflict_sets[v].update(conf)
                return False, conf
            conf.discard(v)
            self.conflict_sets[v].update(conf)
            del self.assignment[v]

        conf = set(self.conflict_sets[v])
        conf.add(v)
        return False, conf

    def solve(self):
        sat, _ = self.search()
        return self.solution if sat else None

def solve_backjumping(c, n): return CBJSolver(c, n).solve()
