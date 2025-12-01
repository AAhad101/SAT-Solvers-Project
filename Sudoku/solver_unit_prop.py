import copy

def solve_unit_prop(board):
    def peers(r, c):
        ps = {(r, i) for i in range(9)} | {(i, c) for i in range(9)}
        br, bc = (r//3)*3, (c//3)*3
        ps |= {(i, j) for i in range(br, br+3) for j in range(bc, bc+3)}
        ps.remove((r, c))
        return ps

    def init_domains():
        d = {}
        for r in range(9):
            for c in range(9):
                d[(r,c)] = {board[r][c]} if board[r][c] else set(range(1,10))
        return d

    def propagate(d):
        changed = True
        while changed:
            changed = False
            for cell, vals in list(d.items()):
                if len(vals) == 1:
                    v = next(iter(vals))
                    for p in peers(*cell):
                        if v in d[p]:
                            d[p].remove(v)
                            if not d[p]:
                                return False
                            changed = True
        return True

    def search(d):
        if not propagate(d):
            return None
        if all(len(v) == 1 for v in d.values()):
            return d
        unassigned = {k: v for k,v in d.items() if len(v) > 1}
        var = min(unassigned, key=lambda k: len(unassigned[k]))
        for val in unassigned[var]:
            nd = copy.deepcopy(d)
            nd[var] = {val}
            res = search(nd)
            if res:
                return res
        return None

    dom = init_domains()
    result = search(dom)
    if not result:
        return False
    for (r,c), vals in result.items():
        board[r][c] = next(iter(vals))
    return True
