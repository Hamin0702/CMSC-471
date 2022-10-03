# CMSC 471 Assignment 1 - Water Jug Problem by Hamin Han

## Problem Statement

There are two jugs J1, J2 with Capacity 5 gal and 2 gal respectively. </br>

**Initial State:** J1 has 4 gallons of water and J2 has 1 gallon of water. </br>

**Actions:**
1. **Pour1** Pour from jug X to jug Y until X empty or Y full. (if Y is already full/X is empty, do not take this action)
2. **Pour2** Pour from jug Y to jug X until X is full or Y is empty.(if X is already full/Y is empty,do not take this action)
3. **Dump1** Empty jug X
4. **Dump2** Empty jug Y

**Goal States:** The goal states that need to be reached are
1. (0,1) (Jug 1 has 0, Jug 2 has 1)
2. (4,0) (Jug 1 has 4, Jug 2 has 0)
3. (5,0) (Jug 1 has 5, Jug 2 has 0)
4. (3,2) (Jug 1 has 3, Jug 2 has 2)
5. (1,2) (Jug 1 has 1, Jug 2 has 2)

## Algorithms
* ### Breadth First Search (BFS)
* ### Depth First Search(DFS) (without tracking seen nodes)
* ### A∗ Algorithm

## Included Files
* ### WaterJug.py
    - The main code to run the algorithms for the water jug problem.
* ### README.md
    - This file that documents details about this project.
* ### output.txt
    - The output text file after running an algorithm
    - Contains, initial state, goal state, strategy, solution path, solution action, and total cost.
* ### HW1 Questions.pdf
    - Has the answers to the word questions of the assignment.
* ### Output Folders
    - Contains the output text files of running the algorithms.

## **Important Notes**
* ### You can run the different strategies in the WaterJug.py main function. Just run the function with the target values (For example, BFS(4,0) runs the BFS function with (4,0) as the target state).
* ### Other than the output text file, running the function will also output messages to the console, showing the initial and goal state, the solution path and actions, as well as the contents of the search queue for each step.
* ### 3 of the DFS goal states will run in an infinite loop. This is because they keep on repeating the same state and it has no memory of it.