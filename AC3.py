import sys
import copy
import numpy as np

rows = "123456789"
cols = "ABCDEFGHI"

# One class that implements AC3 and Backtracking
class SudokuCSP:

    # Class Constructor
    def __init__(self, grid):

        # Items
        # Combine the 2d Array into one list so that it's easier to work with
        self.items = []
        # Iterate with outer list
        for element in grid:
            if type(element) is list:
                # Check if type is list than iterate through the sublist
                for item in element:
                    self.items.append(item)
            else:
                self.items.append(element)

        # Variables
        # Set the variables with the rows and column names
        self.variables = [x + y for x in cols for y in rows]

        # Domains
        # Set the domains with it's actual value or 1-9
        self.domains = dict()
        for i in range(81):
            if self.items[i] == 0:
                self.domains[self.variables[i]] = list(range(1,10)) #1-9 for empty cells
            else:
                self.domains[self.variables[i]] = [self.items[i]] # Domain is the value if the square was already filled out

        # Neighbors
        # Dictionary with the variable as the key and the set of neighboring variables as the value, same row, column, square
        self.unitlist = ([[x + y for x in col for y in rows] for col in cols] +
                        [[x + y for x in cols for y in row] for row in rows] +
                        [[x + y for x in col_box for y in row_box] for col_box in ('ABC', 'DEF', 'GHI') for row_box in ('123', '456', '789')])
        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.variables)
        self.neighbors = dict((s, set(sum(self.units[s],[]))-set([s])) for s in self.variables)

        # Constraints
        # Binary constraints
        self.constraints = [(variable, neighbor) for variable in self.variables for neighbor in self.neighbors[variable]]

        self.ans = copy.deepcopy(grid)

    # Using AC3, solves the sudoku
    def solve(self):
        ac3 = self.AC3()
        
        if self.isComplete() and ac3:
            self.ans = self.getSolvedGrid()
        else:
            assignment = {}

            for cell in self.variables:
                if len(self.domains[cell]) == 1:
                    assignment[cell] = self.domains[cell][0]
            
            # Backtracking
            assignment = self.backtrack(assignment)
            
            for cell in self.domains:
                if len(cell) > 1:
                    self.domains[cell] = assignment[cell] 
            
            if assignment:
                self.ans = self.getSolvedGrid();

        return self.ans

    # AC3 algorithm for Constraint Propagation
    def AC3(self):
        queue = self.constraints

        while queue:

            (x, y) = queue.pop(0)

            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for i in self.neighbors[x]:
                    if i != x:
                        queue.append((i,x))

        return True

    # Revise algorithm used in AC3
    def revise(self, x, y):

        revised = False

        for i in self.domains[x]:

            if not any([(i != j) for j in self.domains[y]]):
            
                # Remove i from x's domain
                self.domains[x].remove(i)
                revised = True

        return revised

    # The recursive backtrack method will assign values after going throw AC3
    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        # Choose next variable
        cell = self.getNextVariable(assignment)
        domain = copy.deepcopy(self.domains)

        # Select the least constraining values for variable
        for x in self.LCV(cell):
            if self.isConsistent(assignment, cell, x):
                assignment[cell] = x
                inferences = {}
                # Begin forward checking
                inferences = self.forwardCheck(assignment, inferences, cell, x)

                if inferences != "Conflict Found":
                    # Recursive Call
                    result = self.backtrack(assignment)
                    if result != "Conflict Found":
                        return result
                del assignment[cell]
                self.domains.update(domain)
        return "Conflict Found"

    # Forward checking with the concept of inferences
    def forwardCheck(self, assignment, inferences, cell, value):
        inferences[cell] = value

        for neighbor in self.neighbors[cell]:
        
            # Case: The value getting assigned to current cell is in the domain of a neighboring variable
            if neighbor not in assignment and value in self.domains[neighbor]:

                # If that value is the very last domain of the neighbor, then there is a conflict
                if len(self.domains[neighbor]) == 1:
                    return "Conflict Found"

                # If there's no conflict, remove from domain
                self.domains[neighbor].remove(value)
                remaining = self.domains[neighbor]

                if len(remaining) == 1:
                    check = self.inference(assignment, inferences, neighbor, remaining)
                    if check == "Conflict Found":
                        return "Conflict Found"

        return inferences

    # Check if the Sudoku is completed, this is true when all the variables have 1 item in their domain
    def isComplete(self):
        for variables, domain in self.domains.items():
            if len(domain) == 1:
                return True
        return False
   
    # Check that the neighboring cells are consistent with the constraints
    def isConsistent(self, assignment, cell, value):
        consistent = True
        
        for curr_cell, curr_value in assignment.items():

            # If neigboring cells have the same value, not consitent
            if curr_value == value and curr_cell in self.neighbors[cell]:
                consistent = False

        return consistent

    # Find the next variable that has fewest values in its domain
    def getNextVariable(self, assignment):
        emptyCells = []

        for cell in self.variables:
            if cell not in assignment:
                emptyCells.append(cell)

        return min(emptyCells, key=(lambda cell: len(self.domains[cell])))

    # Find the Least Constraining Value
    def LCV(self, cell):
        if len(self.domains[cell]) == 1:
            return self.domains[cell]

        return sorted(self.domains[cell], key=(lambda value: self.numConflicts(cell, value)))

    # Find the number of conflicts it has with neighboring cells
    def numConflicts(self, cell, value):
        conflicts = 0
        for neighbor in self.neighbors[cell]:
            # rules out value for neighbors
            if len(self.domains[neighbor]) > 1 and value in self.domains[neighbor]:
                conflicts += 1
        return conflicts

   # Return the solved ans grid
    def getSolvedGrid(self):
        grid = [[0 for i in range(9)] for j in range(9)]
        i = 0
        j = 0

        for c in cols:
            j = 0
            for r in rows:
                grid[i][j] = self.domains[c+r]
                j += 1
                if j > 8:
                    break
            i += 1
            if i > 8:
                break

        return grid

# Create the 2d Array with the initial input string
def setSudokuMatrix(input):
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
    return grid

# Print out the Sudoku Matrix
def getSudokuMatrix(items):
    grid = [[0 for x in range(9)] for y in range(9)]
    y = 0
    x = 0

    for value in items:
        grid[y][x] = value
        x += 1

        if x > 8:
            x = 0
            y += 1
    return grid

"""
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
"""

"""
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
"""

# Main function to take in the input from the commandline
# Example Test Inputs: 
# python AC3.py ”..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..”
# python AC3.py ”...26.7.168..7..9.19...45..82.1...4...46.29...5...3.28..93...74.4..5..367.3.18...”
if __name__ == "__main__":

    # Taking in the input string argument from the command line
    gridInput = sys.argv[1] # the second argument, the input string for unsolved SudokuCSP
    sudokuBoard = setSudokuMatrix(gridInput)
    print(np.matrix(sudokuBoard))
    print()

    # Running the code to solve the Sudoku
    sudoku = SudokuCSP(sudokuBoard)
    ans = sudoku.solve()

    # Display results
    ans = [item for sublist in ans for item in sublist]
    answer = [item for sublist in ans for item in sublist]
    print("Solved SudokuCSP Grid: \n")
    print(np.matrix(getSudokuMatrix(answer)))