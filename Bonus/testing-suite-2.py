import unittest
import sys
import copy
from minesweeper import auto_solve, print_board

# Increase recursion limit for deep DPLL trees
sys.setrecursionlimit(5000)

class TestMinesweeperComprehensive(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None  # Show full diffs on failure

    # --- HELPER FUNCTIONS ---
    def parse_map(self, ascii_map):
        """
        Parses an ASCII grid to create the Solution Board and Starting Board.
        
        Legend:
        'X' : Mine (Hidden initially)
        '.' : Safe (Hidden initially)
        '#' : Safe (Revealed initially)
        
        Returns:
            solution_board: Fully revealed board with numbers (0-8) and mines (9)
            start_board: The player view with -1 for hidden, numbers for revealed, 
                         and checks consistency.
        """
        rows = ascii_map.strip().split('\n')
        rows = [r.strip() for r in rows]
        height = len(rows)
        width = len(rows[0])
        
        solution_board = [[0 for _ in range(width)] for _ in range(height)]
        start_board = [[-1 for _ in range(width)] for _ in range(height)]
        
        # 1. Place Mines
        for r in range(height):
            for c in range(width):
                char = rows[r][c]
                if char == 'X':
                    solution_board[r][c] = 9
                elif char in ['.', '#']:
                    pass # calculated later
                else:
                    raise ValueError(f"Unknown char '{char}' at {r},{c}")

        # 2. Calculate Numbers for Safe Cells
        for r in range(height):
            for c in range(width):
                if solution_board[r][c] == 9:
                    continue
                
                # Count neighbor mines
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0: continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < height and 0 <= nc < width:
                            if solution_board[nr][nc] == 9:
                                count += 1
                solution_board[r][c] = count

        # 3. Create Start Board (Initial Reveal)
        for r in range(height):
            for c in range(width):
                if rows[r][c] == '#':
                    # This cell is initially revealed
                    start_board[r][c] = solution_board[r][c]
                # '.' and 'X' remain -1 (Hidden)

        return solution_board, start_board

    def run_solve(self, ascii_map, expect_success=True, description=""):
        print(f"\nTesting: {description}")
        solution, start = self.parse_map(ascii_map)
        
        print("Initial View:")
        print_board(start)
        
        # We pass a copy because auto_solve modifies in-place
        result = auto_solve(start, solution, debug=False)
        
        if expect_success:
            self.assertTrue(result, f"Failed to solve deterministically: {description}")
            # Ensure no -1 left
            for r in start:
                self.assertNotIn(-1, r, "Board marked solved but contains hidden cells (-1)")
        else:
            self.assertFalse(result, f"Solver solved a guessing scenario (impossible): {description}")

    # --- TESTS ---

    def test_01_corner_logic(self):
        """
        X . . 
        . . .
        # . .
        
        We reveal the bottom left. The logic must wrap around the corner.
        """
        grid = """
        X..
        ...
        #..
        """
        self.run_solve(grid, True, "Corner Mine Logic")

    def test_02_tunnel_logic(self):
        """
        X X .
        . . .
        # . .
        
        A wall of mines. The solver must deduce the boundary.
        """
        grid = """
        XX.
        ...
        #..
        """
        self.run_solve(grid, True, "Mine Wall/Tunnel")

    def test_03_surrounded_eight(self):
        """
        X X X
        X . X
        X X X
        
        The middle cell is an '8'. If we reveal it (conceptually), 
        the solver must flag all neighbors immediately.
        """
        grid = """
        XXX
        X#X
        XXX
        """
        self.run_solve(grid, True, "Surrounded by 8 Mines")

    def test_04_guessing_deadlock(self):
        """
        X .
        . .
        
        Revealing bottom right gives a '1'. 
        Top Left and Top Right are equally likely. Solver MUST fail.
        """
        grid = """
        X.
        .#
        """
        self.run_solve(grid, False, "Classic 50/50 Guess")

    def test_05_121_pattern(self):
        """
        X X X
        . . .
        # # #
        
        Standard 1-2-1 Pattern.
        Row 1 will be: 2 3 2.
        Solver should deduce row 0 are all mines.
        """
        grid = """
        XXX
        ...
        ###
        """
        self.run_solve(grid, True, "1-2-1 Pattern")

    def test_06_1221_pattern(self):
        """
        . X X .
        . . . .
        # # # #
        
        1-2-2-1 Pattern implies mines are under the 2s.
        """
        grid = """
        .XX.
        ....
        ####
        """
        self.run_solve(grid, True, "1-2-2-1 Pattern")

    def test_07_disconnected_islands(self):
        """
        X . . . X
        . . . . .
        # . . . #
        
        Two separate problems on one board. 
        Solver should handle both sides.
        """
        grid = """
        X...X
        .....
        #...#
        """
        self.run_solve(grid, True, "Disconnected Islands")

    def test_08_long_rectangle(self):
        """
        Non-square board test.
        """
        grid = """
        X.X.X.X.
        ........
        ########
        """
        self.run_solve(grid, True, "Long Rectangular Board (8x3)")

    def test_09_the_hole(self):
        """
        X X X
        X . X
        X X X
        
        Wait, this is the 8 case. Let's try the inverse (The Safe Island).
        . . .
        . # .
        . . .
        
        Revealing the center '0' should cascade the whole board.
        """
        grid = """
        ...
        .#.
        ...
        """
        self.run_solve(grid, True, "Safe Island / Zero Cascade")

    def test_10_complex_interaction(self):
        """
        A slightly messier board requiring multiple steps of inference.
        X X . .
        . . . . 
        . . X .
        # # # #
        """
        grid = """
        XX..
        ....
        ..X.
        ####
        """
        self.run_solve(grid, True, "Complex Asymmetric Layout")

if __name__ == '__main__':
    unittest.main()
