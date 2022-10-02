class Jug:

    def __init__(self, jug1, jug2, action, parent):
        self.jugs = (jug1,jug2)
        self.jug1 = jug1
        self.jug2 = jug2
        self.action = action
        self.parent = parent
        self.isStart = False
        self.hval = 1
        self.astarscore = 1

    def startTrue(self, bool):
        self.isStart = bool

    def addAstarscore(self, val):
        self.astarscore = self.astarscore + val

    def __repr__(self):
        return f"{self.jugs}"

# Function for BFS
def BFS(target):

    # Initial states of the jugs
    jugX = 4
    jugY = 2
    j1cap = 5
    j2cap = 2
    start = Jug(jugX,jugY,None,None)
    start.startTrue(True)

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

def DFS(target):
    None

def Astar(target):
    None

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

# Driver
if __name__ == '__main__':
    
    # BFS
    # BFS((0,1))
    # BFS((4,0))
    # BFS((5,0))
    BFS((3,2))
    # BFS((1,2))