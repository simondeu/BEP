class Node():
    
    def __init__(self, name, neighbours, type):
        self.name = name
        self.neighbours = neighbours
        self.type = ""
        
    def __str__(self):
        return self.name
    
    def __name__(self):
        return self.name
    
class Edge():
    
    def __init__(self, u, v):
        self.u = u
        self.v = v
        self.name = u.name + v.name
        self.type = ""
        self.direction = None

def GetAB(u,v,A):
    A.append(u)
    for node in u.neighbours:
        if node not in A and node != v:
            A = GetAB(node,u,A)
    return A

def CheckABx(A,B,Leaf):
    for i in A:
        for x1 in B:
            for x2 in B:
                if x1 != x2:
                    if ((i,Leaf),(x1,x2)) not in Splits:
                        return False
    return True

def StrongEdgeStem(Edge):
    Edge.type = "StrongEdge"

def DirectedEdge(Edge, Direction):
    Edge.type = "Directed"
    Edge.direction = Direction

def WeakStemEdge(Edge):
    Edge.type = "WeakEdge"

def FindStem(Leaf):
    for Edge in NetworkEdges:
        A = GetAB(Edge.u,Edge.v,[])
        B = GetAB(Edge.v,Edge.u,[])

        Ac = CheckABx(A,B,Leaf)
        Bc = CheckABx(B,A,Leaf)
        print(Ac, Bc)
    
        if Ac and Bc:
            StrongEdgeStem(Edge)
        elif Ac and not Bc:
            DirectedEdge(Edge, Edge.u)
        elif Bc and not Ac:
            DirectedEdge(Edge, Edge.v)
        elif not Ac and not Bc:
            WeakStemEdge(Edge)

def GetNextEdge(edge):
    for i in NetworkEdges:
        if i.u is edge.direction or i.v is edge.direction:
            if i.direction is not edge.direction:
                return i
    return edge.direction

def WeakEdgeConstructor(Edges):
    pass

def ConstructNetwork(NewLeaf):
    
    weakEdges = []

    for edge in NetworkEdges:
        if edge.type == "StrongEdge":
            NetworkEdges.remove(edge)
            global InternalNodes
            InternalNodes += 1
            InternalNode = Node("InternalNode"+str(InternalNodes), [edge.u,edge.v,NewLeaf],"Internal")
            NetworkLeaves.append(InternalNode)
            NetworkLeaves.append(NewLeaf)
            NetworkEdges.append(Edge(edge.u,InternalNode))
            NetworkEdges.append(Edge(edge.v,InternalNode))
            NetworkEdges.append(Edge(NewLeaf,InternalNode))
            return
        if edge.type == "WeakEdge":
            weakEdges.append(edge)

    if len(weakEdges) is not 0:
        WeakEdgeConstructor(weakEdges)

    constructing = True
    edge = NetworkEdges[0]
    while constructing:
        edge = GetNextEdge(edge)
        if type(edge) is not Edge:
            constructing = False

        
#Reading the file and constructing a set of leaves and a set of the splits of the network

with open( "Test.txt") as f:
    lines = f.readlines()

Leaves = []
TempLeaves = lines[0].split("(")[1].split(")")[0].split(",")
for i in TempLeaves:
    Leaves.append(Node(i,[],"Leaf"))

Splits = []
for i in range(1,len(lines)):
    line = lines[i]
    Splits.append(((line[1],line[3]),(line[5],line[7])))
    

NetworkLeaves = []
NetworkEdges = []
InternalNodes = 0

#Step 1: Creating the first edge of the network
Leaves[0].neighbours.append(Leaves[1]), NetworkLeaves.append(Leaves[0])
Leaves[1].neighbours.append(Leaves[0]), NetworkLeaves.append(Leaves[1])
NetworkEdges.append(Edge(Leaves[0],Leaves[1]))

#Leaves[2].neighbours.append(Leaves[0]), Leaves[0].neighbours.append(Leaves[2])

#Step 2: Find stem for next leaf

for i in range(1,5):#len(Leaves)-1):
    FindStem(Leaves[i+1])
    ConstructNetwork(Leaves[i+1])
    
for i in NetworkEdges:
    print(i.name, i.direction) 

for i in NetworkLeaves:
    print(i.name)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    