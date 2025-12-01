import sys
import unittest
# Import the logic from your file
from minesweeper import auto_solve, print_board

class TestMinesweeperSAT(unittest.TestCase):

    def setUp(self):
        # Increase recursion limit because custom DPLL 
        # is recursive and might go deep on larger boards
        sys.setrecursionlimit(2000)

    def create_game_state(self, full_solution, revealed_coords):
        """
        Helper to create the player's view (start_board) based on 
        the full solution and a list of initially revealed coordinates.
        """
        rows = len(full_solution)
        cols = len(full_solution[0])
        
        # Initialize with -1 (hidden)
        start_board = [[-1 for _ in range(cols)] for _ in range(rows)]
        
        for r, c in revealed_coords:
            start_board[r][c] = full_solution[r][c]
            
        return start_board

    def test_01_simple_corner(self):
        print("\n--- Test 1: Simple 3x3 Corner ---")
        # 9 is Mine. 
        # A mine in top-left, surrounded by 1s.
        solution = [
            [9, 1, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]
        # We reveal the bottom right 0. This should cascade logically.
        start = self.create_game_state(solution, [(2, 2)])
        
        print("Initial State:")
        print_board(start)
        
        result = auto_solve(start, solution, debug=False)
        self.assertTrue(result, "Solver should solve a simple corner deterministic board")

    def test_02_the_1_2_1_pattern(self):
        print("\n--- Test 2: The 1-2-1 Logic Pattern ---")
        # A classic logic pattern: 1-2-1 usually implies mines are under the 1s.
        # Board:
        # 9 9 9 (Row 0 - mines)
        # 2 3 2 (Row 1)
        # 0 0 0 (Row 2 - Safe)
        solution = [
            [9, 9, 9],
            [2, 3, 2],
            [0, 0, 0]
        ]
        
        # We reveal the bottom row of zeros and the numbers
        start = self.create_game_state(solution, [
            (2,0), (2,1), (2,2), # Safe bottom
            (1,0), (1,1), (1,2)  # The numbers 2, 3, 2
        ])
        
        print("Initial State:")
        print_board(start)
        
        result = auto_solve(start, solution, debug=False)
        self.assertTrue(result, "Solver should deduce the mines in the top row")
        # Verify top row is flagged (9)
        self.assertEqual(start[0], [9, 9, 9])

    def test_03_trivial_empty(self):
        print("\n--- Test 3: All Safe Board ---")
        solution = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        start = self.create_game_state(solution, [(1, 1)]) # Reveal middle
        
        result = auto_solve(start, solution, debug=False)
        self.assertTrue(result)

    def test_04_guessing_required(self):
        print("\n--- Test 4: Guessing Required (Solver Should Stuck) ---")
        # A 2x2 board where we can't distinguish.
        # 9 0
        # 1 1
        # If we reveal (1,0)=1 and (1,1)=1, we know there is 1 mine in the top row.
        # But we don't know if it's left or right.
        
        solution = [
            [9, 0],
            [1, 1]
        ]
        start = self.create_game_state(solution, [(1, 0), (1, 1)])
        
        print("Initial State:")
        print_board(start)
        
        result = auto_solve(start, solution, debug=False)
        self.assertFalse(result, "Solver should return False when stuck/guessing is needed")
        
        # Verify it didn't wrongly flag anything in top row
        self.assertEqual(start[0][0], -1) 
        self.assertEqual(start[0][1], -1)

    def test_05_medium_board(self):
        print("\n--- Test 5: Medium 6x6 Deterministic ---")
        # A larger board to stress the DPLL recursion slightly
        solution = [
            [0, 0, 1, 9, 1, 0],
            [0, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0],
            [1, 9, 1, 0, 1, 1],
            [1, 1, 1, 0, 1, 9]
        ]
        # Reveal a safe patch in the middle
        start = self.create_game_state(solution, [(2, 2), (2, 3)])
        
        print("Initial State:")
        print_board(start)
        
        result = auto_solve(start, solution, debug=False)
        self.assertTrue(result, "Solver should handle a medium deterministic board")

if __name__ == '__main__':
    unittest.main()
