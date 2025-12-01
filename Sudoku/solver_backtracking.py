def solve_backtracking(board):
    def is_valid(b, r, c, num):
        for i in range(9):
            if b[r][i] == num or b[i][c] == num:
                return False
        br, bc = (r // 3) * 3, (c // 3) * 3
        return all(b[i][j] != num for i in range(br, br+3) for j in range(bc, bc+3))

    def find_empty(b):
        for r in range(9):
            for c in range(9):
                if b[r][c] == 0:
                    return r, c
        return None

    pos = find_empty(board)
    if not pos:
        return True
    r, c = pos

    for num in range(1, 10):
        if is_valid(board, r, c, num):
            board[r][c] = num
            if solve_backtracking(board):
                return True
            board[r][c] = 0
    return False
