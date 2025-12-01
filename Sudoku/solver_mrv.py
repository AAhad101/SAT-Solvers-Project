def solve_mrv(board):
    def valid_values(b, r, c):
        vals = set(range(1, 10))
        vals -= set(b[r])
        vals -= {b[i][c] for i in range(9)}
        br, bc = (r//3)*3, (c//3)*3
        vals -= {b[i][j] for i in range(br, br+3) for j in range(bc, bc+3)}
        return vals

    def select_mrv(b):
        best, best_vals = None, None
        min_size = 10
        for r in range(9):
            for c in range(9):
                if b[r][c] == 0:
                    vals = valid_values(b, r, c)
                    if not vals:
                        return (r, c), []
                    if len(vals) < min_size:
                        min_size = len(vals)
                        best, best_vals = (r, c), vals
        return best, best_vals

    cell, vals = select_mrv(board)
    if cell is None:
        return True
    if not vals:
        return False

    r, c = cell
    for v in vals:
        board[r][c] = v
        if solve_mrv(board):
            return True
        board[r][c] = 0
    return False
