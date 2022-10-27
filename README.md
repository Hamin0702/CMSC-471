# CMSC 471 Assignment 1 - Water Jug Problem by Hamin Han

## **Background**

A Sudoku puzzle is a 9x9 grid (81 variables) where each cell in the grid can
take on the integer values 1-9 (the domain of each variable). A solution to a Sudoku puzzle is an assignment of values for each cell in the grid such that no two cells in the same row,
column, or 3x3 square have the same value. </br>

In this assignment, you have to model a unsolved Sudoku puzzle as CSP and then solve it
using the Constraint Propagation (AC3 algorithm) and Backtracking Search. In AC3,
you need to check arc consistency and enforce arc consistency by removing values from
the domain of unassigned variables </br>

### **Input:**
Your program should take an unsolved Sudoku Grid as input. The input will be given as a continuous string of 81 characters. The unassigned cells will be marked with a ”.” The input string is the join of consecutive rows. </br>
For example, the input to your program would be </br>
"..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.." </br>

### **Output**
Your program should print the nal output as a 9x9 grid. </br>

### **Testing**
To test your program, you may use the following inputs:
* "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
* "...26.7.168..7..9.19...45..82.1...4...46.29...5...3.28..93...74.4..5..367.3.18..."

## Included Files

* ### AC3.py
    - The main python file that solves the Sudoku
    - run the program by typing into the command prompt: python AC3.py "Input-Values"
* ### README.md
    - This file that documents details about this project.