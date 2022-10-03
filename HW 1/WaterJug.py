# Used for DFS timeout functionality
import time
timeout = time.time() + 0.1

# Class for a node of a state with its jugs
class Jug:

    # Constructor
    def __init__(self, jug1, jug2, action, parent):
        self.jugs = (jug1,jug2)
        self.jug1 = jug1
        self.jug2 = jug2
        self.action = action
        self.parent = parent
        self.isStart = False

        # Values used for Astar
        self.gval = 0
        self.hval = 0
        self.astarscore = 0

    # Set true for the starting node
    def startTrue(self, bool):
        self.isStart = bool

    def __repr__(self):
        return f"{self.jugs}"

# Global values for the initial state of the jugs
jugX = 4
jugY = 1
j1cap = 5
j2cap = 2
start = Jug(jugX,jugY,None,None)
start.startTrue(True)

# Function for BFS
def BFS(target):

    # Target state
    T = target

    # Queue of the Jugs states
    queue = []
    queue.append(start)
    
    # Memory list
    visited = []

    # Solution lists
    path = []
    moves = []

    # Final solution state
    goal = None

    print("Initial State: (%d,%d)" % (jugX, jugY))
    print("Goal State: (%d,%d)" % (target[0], target[1]))
    print("Contents of the search")

    while len(queue) > 0:

        # Graphical representation of the queue
        print(queue)

        # Current state
        current = queue.pop(0)

        # If it reaches the goal state
        if current.jugs == T:
            print("Solution Found!")
            goal = current
            break

        # Skip if the state has been visited
        if current.jugs in visited:
            continue

        # Error checking
        if current.jug1 < 0 or current.jug2 < 0 or current.jug1 > j1cap or current.jug2 > j2cap:
            continue
        # Skip if it's at (0,0), no action possible
        elif current.jug1 == 0 and current.jug2 == 0:
            continue

        # Add to visited
        visited.append(current.jugs)

        # Case 1: Pour Jug 1 to Jug 2
        if current.jug1 != 0 and current.jug2 < j2cap:

            # Values for the new state of jugs
            if current.jug1 + current.jug2 <= j2cap:
                jug1 = 0
                jug2 = current.jug1 + current.jug2
            else:
                jug1 = current.jug1 + current.jug2 - j2cap
                jug2 = j2cap
           
            if (jug1,jug2) not in visited:
                queue.append(Jug(jug1,jug2,"Pour 1",current))

        # Case 2: Pour Jug 2 to Jug 1
        if current.jug1 < j1cap and current.jug2 != 0:

            # Values for the new state of jugs
            if current.jug1 + current.jug2 <= j1cap:
                jug1 = current.jug1 + current.jug2
                jug2 = 0
            else:
                jug1 = j1cap
                jug2 = current.jug1 + current.jug2 - j1cap

            if (jug1,jug2) not in visited:
                queue.append(Jug(jug1,jug2,"Pour 2",current))

        # Case 3: Empty Jug 1
        if current.jug1 > 0 and (0,current.jug2) not in visited:
            queue.append(Jug(0,current.jug2,"Dump 1",current))

        # Case 4: Empty Jug 2
        if current.jug2 > 0 and (current.jug1,0) not in visited:
            queue.append(Jug(current.jug1,0,"Dump 2",current))

    if goal == None:
        raise Exception("Goal Doesn't exist")

    # Finding the path and the moves
    traverse = goal
    path.append(traverse.jugs)
    moves.append(traverse.action)
    while True:
        if(traverse.parent.isStart):
            traverse = traverse.parent
            path.append(traverse.jugs)
            break
        traverse = traverse.parent
        path.append(traverse.jugs)
        moves.append(traverse.action)

    path.reverse()
    moves.reverse()

    print("Solution Path:")
    print(path)
    print("Solution action:")
    print(moves)

    # Create Output.txt based on the algorithm
    outputText("BFS", start.jugs, target, path, moves)

# Function for DFS *No memory
def DFS(target):

    # Target state
    T = target

    # Queue of the Jugs states
    queue = []
    queue.append(start)
    
    # Solution lists
    path = []
    moves = []

    # Final solution state
    goal = None

    print("Initial State: (%d,%d)" % (jugX, jugY))
    print("Goal State: (%d,%d)" % (target[0], target[1]))
    print("Contents of the search")

    while len(queue) > 0:

        if time.time() > timeout:
            timeoutputText("DFS", start.jugs, target)
            raise Exception("TIME OUT: Infinite Loop in DFS")

        # Graphical representation of the queue
        print(queue)

        # Current state
        current = queue.pop(0)

        # If it reaches the goal state
        if current.jugs == T:
            print("Solution Found!")
            goal = current
            break

        # Error checking
        if current.jug1 < 0 or current.jug2 < 0 or current.jug1 > j1cap or current.jug2 > j2cap:
            continue
        # Skip if it's at (0,0), no action possible
        elif current.jug1 == 0 and current.jug2 == 0:
            continue

        # Instead of queing the next states 1-4 to the end of the queue, 
        # now add them to the front so that it evaluates depth first
        # Goes in reverse order and add it to the front of the queue 
        # so 1-4 will stack on top of what's already in the queue before

        # Case 4: Empty Jug 2
        if current.jug2 > 0:
            queue.insert(0,(Jug(current.jug1,0,"Dump 2",current)))

        # Case 3: Empty Jug 1
        if current.jug1 > 0:
            queue.insert(0,(Jug(0,current.jug2,"Dump 1",current)))

        # Case 2: Pour Jug 2 to Jug 1
        if current.jug1 < j1cap and current.jug2 != 0:

            # Values for the new state of jugs
            if current.jug1 + current.jug2 <= j1cap:
                jug1 = current.jug1 + current.jug2
                jug2 = 0
            else:
                jug1 = j1cap
                jug2 = current.jug1 + current.jug2 - j1cap

            queue.insert(0,(Jug(jug1,jug2,"Pour 2",current)))

        # Case 1: Pour Jug 1 to Jug 2
        if current.jug1 != 0 and current.jug2 < j2cap:

            # Values for the new state of jugs
            if current.jug1 + current.jug2 <= j2cap:
                jug1 = 0
                jug2 = current.jug1 + current.jug2
            else:
                jug1 = current.jug1 + current.jug2 - j2cap
                jug2 = j2cap
           
            queue.insert(0,(Jug(jug1,jug2,"Pour 1",current)))

    if goal == None:
        raise Exception("Goal Doesn't exist")

    # Finding the path and the moves
    traverse = goal
    path.append(traverse.jugs)
    moves.append(traverse.action)
    while True:
        if(traverse.parent.isStart):
            traverse = traverse.parent
            path.append(traverse.jugs)
            break
        traverse = traverse.parent
        path.append(traverse.jugs)
        moves.append(traverse.action)

    path.reverse()
    moves.reverse()

    print("Solution Path:")
    print(path)
    print("Solution action:")
    print(moves)

    # Create Output.txt based on the algorithm
    outputText("DFS", start.jugs, target, path, moves)

# function for Astar
def Astar(target):

     # Target state
    T = target

    # Queue of the Jugs states
    queue = []
    queue.append(start)
    
    # Memory list
    visited = []

    # Solution lists
    path = []
    moves = []

    # Final solution state
    goal = None

    print("Initial State: (%d,%d)" % (jugX, jugY))
    print("Goal State: (%d,%d)" % (target[0], target[1]))
    print("Contents of the search")

    while len(queue) > 0:

        # Sort the list with the lowest A* score first
        queue.sort(key=lambda x: x.astarscore)

        # Graphical representation of the queue
        print(queue)

        # Current state
        current = queue.pop(0)

        # If it reaches the goal state
        if current.jugs == T:
            print("Solution Found!")
            goal = current
            break

        # Skip if the state has been visited
        if current.jugs in visited:
            continue

        # Add to visited
        visited.append(current.jugs)    

        # Error checking
        if current.jug1 < 0 or current.jug2 < 0 or current.jug1 > j1cap or current.jug2 > j2cap:
            continue
        # Skip if it's at (0,0), no action possible
        elif current.jug1 == 0 and current.jug2 == 0:
            continue
        # Skip if the water in the current jugs is less than what we need for the target
        elif current.jug1 + current.jug2 < target[0] + target[1]:
            continue

        # Case 1: Pour Jug 1 to Jug 2
        if current.jug1 != 0 and current.jug2 < j2cap:

            # Values for the new state of jugs
            if current.jug1 + current.jug2 <= j2cap:
                jug1 = 0
                jug2 = current.jug1 + current.jug2
            else:
                jug1 = current.jug1 + current.jug2 - j2cap
                jug2 = j2cap
           
            if (jug1,jug2) not in visited:
                newState = Jug(jug1,jug2,"Pour 1",current)
                calculateAstarScore(newState,target)
                queue.append(newState)

        # Case 2: Pour Jug 2 to Jug 1
        if current.jug1 < j1cap and current.jug2 != 0:

            # Values for the new state of jugs
            if current.jug1 + current.jug2 <= j1cap:
                jug1 = current.jug1 + current.jug2
                jug2 = 0
            else:
                jug1 = j1cap
                jug2 = current.jug1 + current.jug2 - j1cap

            if (jug1,jug2) not in visited:
                newState = Jug(jug1,jug2,"Pour 2",current)
                calculateAstarScore(newState,target)
                queue.append(newState)

        # Case 3: Empty Jug 1
        if current.jug1 > 0 and (0,current.jug2) not in visited:
            newState = Jug(0,current.jug2,"Dump 1",current)
            calculateAstarScore(newState,target)
            queue.append(newState)

        # Case 4: Empty Jug 2
        if current.jug2 > 0 and (current.jug1,0) not in visited:
            newState = Jug(current.jug1,0,"Dump 2",current)
            calculateAstarScore(newState,target)
            queue.append(newState)

    if goal == None:
        raise Exception("Goal Doesn't exist")

    # Finding the path and the moves
    traverse = goal
    path.append(traverse.jugs)
    moves.append(traverse.action)
    while True:
        if(traverse.parent.isStart):
            traverse = traverse.parent
            path.append(traverse.jugs)
            break
        traverse = traverse.parent
        path.append(traverse.jugs)
        moves.append(traverse.action)

    path.reverse()
    moves.reverse()

    print("Solution Path:")
    print(path)
    print("Solution action:")
    print(moves)

    # Create Output.txt based on the algorithm
    outputText("Astar", start.jugs, target, path, moves)

# function for calculating the Astar score and updating the state node
def calculateAstarScore(state, target):

    # f(n) = g(n) + h(n)
    # f(n) Astar score
    # g(n) = cost it took from start state to this state
    # h(n) = estimate cost to the goal state
    
    # Update g(n), leave as 0 for the start node
    if not state.isStart:
        state.gval = state.gval + 1

    # h(n) is 0 for the goal state
    if state.jug1 == target[0] and state.jug2 == target[1]:
        state.hval == 0
    # Set h(n), if total amount of water in jugs equal total amount of water in goal state, estimate 1 (always less than or equal to actual cost)
    elif state.jug1 + state.jug2 == target[0] + target[1]:
        state.hval = 1
    # Estimate 1 if only need to dump one jug to reach target
    elif (state.jug1 == target[0] and target[1] == 0) or (state.jug2 == target[1] and target[0] == 0):
        state.hval = 1
    # Estimate 2 for everything else
    else:
        state.hval = 2

    # Calculate the final Astar score
    state.astarscore = state.gval + state.hval

# calculate 
# function to output the text file
def outputText(algorithm, initial, goal, solutionPath, solutionMoves):
    
    # Opening text file and writing the initial message
    output = open("output.txt","w")
    output.write("Initial State: (%d,%d)\n" % (initial[0], initial[1]))
    output.write("Goal State: (%d,%d)\n\n" % (goal[0], goal[1]))
    output.write("Serching strategy: " + algorithm + "\n")

    delimiter = ', '
    # Solution Path
    output.write("Path: ")
    output.write(delimiter.join([str(state) for state in solutionPath]))

    # Solution Action
    output.write("\nAction: ")
    output.write(delimiter.join(solutionMoves))

    # Solution Cost
    cost = str(len(solutionMoves))
    output.write("\nCost: " + cost)
    output.close()

# function to output the text file in case of an infinite loop in DFS
def timeoutputText(algorithm, initial, goal):
    
    # Opening text file and writing the initial message
    output = open("output.txt","w")
    output.write("Initial State: (%d,%d)\n" % (initial[0], initial[1]))
    output.write("Goal State: (%d,%d)\n\n" % (goal[0], goal[1]))
    output.write("Serching strategy: " + algorithm + "\n")

    # Time out message
    output.write("Time out due to infinite loop in DFS algorithm \n")
    output.write("Never finds the solution \n")

    output.close()

# Driver
if __name__ == '__main__':
    
    # BFS
    BFS((0,1))
    # BFS((4,0))
    # BFS((5,0))
    # BFS((3,2))
    # BFS((1,2))

    # DFS
    # DFS((0,1)) # INFITE LOOP 
    # DFS((4,0)) # INFITE LOOP 
    # DFS((5,0)) # REACHES GOAL
    # DFS((3,2)) # REACHES GOAL
    # DFS((1,2)) # INFITE LOOP 

    # A star
    # Astar((0,1))
    # Astar((4,0))
    # Astar((5,0))
    # Astar((3,2))
    # Astar((1,2))
