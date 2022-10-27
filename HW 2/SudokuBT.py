import sys
import numpy as np

# Check if the value is valid
def possible(x, y, n):
    for i in range(0, 9):
        if grid[i][x] == n and i != y: # Checks for number (n) in X columns
            return False

    for i in range(0, 9):
        if grid[y][i] == n and i != x: # Checks for number (n) in X columns
            return False

    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for X in range(x0, x0 + 3):
        for Y in range(y0, y0 + 3):  # Checks for numbers in box(no matter the position, it finds the corner)
            if grid[Y][X] == n:
                return False    
    return True

def solve(grid):
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(x, y, n):
                        grid[y][x] = n
                        solve(grid)
                        grid[y][x] = 0
                return
    print(np.matrix(grid))

# Main function to take in the input from the commandline
# Example Test Inputs: 
# python AC3.py ”..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..”
# python AC3.py ”...26.7.168..7..9.19...45..82.1...4...46.29...5...3.28..93...74.4..5..367.3.18...”
if __name__ == "__main__":

    gridInput = sys.argv[1] # the second argument, the input string for unsolved Sudoku

    grid = [[0 for x in range(9)] for y in range(9)]

    y = 0
    x = 0
    for char in gridInput:

        if char != '.':
            grid[y][x] = int(char)
        x += 1

        if x > 8:
            x = 0
            y += 1
    print("Unsolved Sudoku Grid: \n")
    print(np.matrix(grid))

    print()
    solve(grid)