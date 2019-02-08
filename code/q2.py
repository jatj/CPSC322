class Node:
    def __init__(self, name, value=None, depth = 0, values = []):
        self.adjacents = []
        self.name = name
        self.value = value
        self.depth = depth
        self.values = values.copy()
        if depth > 0:
            self.values[depth-1] = value

    def description(self):
        if self.depth == 0:
            return ""
        return "{}={}".format(self.name,self.value)

    def link(self, node):
        self.adjacents.append(node)


def generateTree(useHeuristic = False, file = None):
    Domain = [1,2,3,4]
    varNames = ['A','B','C','D','E','F','G','H']
    mapVarNames = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}
    varN = len(varNames)
    constraints = {
        'AG':lambda A, G : A >= G,
        'AH':lambda A, H : A < H,
        'FB':lambda F, B : abs(F-B) == 1,
        'GH':lambda G, H : G < H,
        'GC':lambda G, C : abs(G-C) == 1,
        'HC':lambda H, C : abs(H-C) % 2 == 0,
        'HD':lambda H, D : H != D,
        'DG':lambda D, G : D >= G,
        'DC':lambda D, C : D != C,
        'EC':lambda E, C : E != C,
        'ED':lambda E, D : E < D-1,
        'EH':lambda E, H : E != H-2,
        'GF':lambda G, F : G != F,
        'HF':lambda H, F : H != F,
        'CF':lambda C, F : C != F,
        'DF':lambda D, F : D != F,
        'EF':lambda E, F : abs(E-F) % 2 == 1,
    }
    # Helper that check if constraints are valid for the provided values
    def checkConstraints(values):
        for key, constraint in constraints.items():
            X = values[mapVarNames[key[0]]]
            Y = values[mapVarNames[key[1]]]
            if X == None:
                continue
            if Y == None:
                continue
            if not constraint(X,Y):
                return False
        return True
    
    # Helper to change the order we pick the variables
    def varNamesByHeuristic():
        heuristics = {}
        newNames = []
        mapNewNames = {}
        for i in range(varN):
            varName = varNames[i]
            heuristics.update({varName:0})
            for key, constraint in constraints.items():
                if varName in key:
                    heuristics[varName] += 1
        i = 0
        for key in sorted(heuristics.keys(), reverse=True):
            mapNewNames.update({key: i})
            newNames.append(key)
            i += 1

        return newNames, mapNewNames

    root = Node("Root", values=[None]*8)
    frontier = [root]
    solutions = []
    fails = 0
    newLine = False
    if useHeuristic:
        varNames,mapVarNames = varNamesByHeuristic()
    f = None
    if file != None:
        f = open(file,"w+")

    while(len(frontier)>0):
        n = frontier.pop()
        # Print the node description (Variable=Value)
        if n.depth > 0:
            nTabs = 1
            if newLine:
                nTabs = n.depth
                newLine = False
            description = "{}{}".format("\t"*nTabs, n.description())
            
            if file != None:
                f.write(description)
            else:
                print(description, end="")
        
        # Check if the current assigned variables are valid with constraints
        if not checkConstraints(n.values):
            if file != None:
                f.write("failure\n")
            else:
                print("failure")
            fails += 1
            newLine = True
            continue

        # Check if we hit a solution
        if n.depth == varN:
            if file != None:
                f.write("solution\n")
            else:
                print("solution")
            solutions.append(n.values)
            newLine = True
            continue

        # Add next variable with all domains
        for i in range(len(Domain)):
            new = Node(varNames[n.depth], Domain[i], n.depth+1, n.values)
            n.link(new)
            frontier.append(new)
    f.close()
    return varNames, solutions, fails

if __name__ == "__main__":
    # variables, solutions, fails = generateTree(False, "../data/q2_tree.txt")
    variables, solutions, fails = generateTree(True, "../data/q2_tree_heur.txt")
    varN = len(variables)

    print("\nNumber of fails: {}".format(fails))
    print("\nNumber of Solutions: {}".format(len(solutions)))
    # Print the solutions
    print("\nSolutions:\n")
    for i in range(varN):
        print("\t{}".format(variables[i]),end="")
    print()
    for i in range(len(solutions)):
        for j in range(varN):
            print("\t{}".format(solutions[i][j]),end="")
        print()