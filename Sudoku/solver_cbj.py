def solve_backjumping(board):
    cells = [(r,c) for r in range(9) for c in range(9) if board[r][c] == 0]
    if not cells:
        return True

    idx = {cell: i for i,cell in enumerate(cells)}
    var_peers = {i: [] for i in range(len(cells))}
    fixed_peers = {i: [] for i in range(len(cells))}

    for i,(r,c) in enumerate(cells):
        peers = {(r,x) for x in range(9)} | {(x,c) for x in range(9)}
        br,bc = (r//3)*3, (c//3)*3
        peers |= {(x,y) for x in range(br, br+3) for y in range(bc, bc+3)}
        peers.discard((r,c))

        for pr,pc in peers:
            if (pr,pc) in idx:
                var_peers[i].append(idx[(pr,pc)])
            elif board[pr][pc] != 0:
                fixed_peers[i].append((pr,pc))

    conflict_sets = {}

    def solve(i):
        if i == len(cells):
            return True
        r,c = cells[i]
        conflict_sets[i] = set()

        for val in range(1,10):
            conflict = False
            tmp_conf = set()

            for fr,fc in fixed_peers[i]:
                if board[fr][fc] == val:
                    conflict = True; break
            if conflict: continue

            for j in var_peers[i]:
                if j < i:
                    rr,cc = cells[j]
                    if board[rr][cc] == val:
                        conflict = True
                        tmp_conf.add(j)
            if conflict:
                conflict_sets[i] |= tmp_conf
                continue

            board[r][c] = val
            res = solve(i+1)
            if res is True:
                return True
            board[r][c] = 0

            if isinstance(res, int):
                if res == i:
                    continue
                return res

        if not conflict_sets[i]:
            return None
        target = max(conflict_sets[i])
        if target in conflict_sets:
            conflict_sets[target] |= conflict_sets[i]
            conflict_sets[target].discard(target)
        return target

    res = solve(0)
    return res is True
