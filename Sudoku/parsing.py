def parse_sudoku_file(filepath):
    boards = []
    try:
        with open(filepath, 'r') as f:
            tokens = f.read().replace('.', '0').split()

        current = []
        for token in tokens:
            if token.startswith('[') or token.endswith(']'):
                continue
            if token.isdigit():
                current.append(int(token))
                if len(current) == 81:
                    boards.append([current[i:i+9] for i in range(0, 81, 9)])
                    current = []
        return boards
    except FileNotFoundError:
        print(f"Error: File not found {filepath}")
        return []

def boards_match(b1, b2):
    return all(b1[r][c] == b2[r][c] for r in range(9) for c in range(9))
