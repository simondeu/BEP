class Node():
    
    def __init__(self, name, neighbours, type):
        self.name = name
        self.neighbours = neighbours
        self.type = ""
        self.coordinate = (0,0)
        self.colour = (0,0,0)
        
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

def GetAB(u,v,Set_):
    Set_.append(u)
    for node in u.neighbours:
        if node not in Set_ and node is not v:
            Set_ = GetAB(node,u,Set_)
    return Set_

def CheckABx(A,B,Leaf):
    for i in A:
        if i in Leaves:
            for x1 in B:
                for x2 in B:
                    if x1 != x2 and x1 in Leaves and x2 in Leaves:
                        if ({i.name,Leaf.name},{x1.name,x2.name}) not in Splits and ({x1.name,x2.name},{i.name,Leaf.name}) not in Splits:
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

def WeakEdgeConstructor(Edges, newLeaf):
    TempLeaves = []
    global InternalNodes
    for i in Edges:
        if i.u not in TempLeaves:
            TempLeaves.append(i.u)
        if i.v not in TempLeaves:
            TempLeaves.append(i.v)
    TempNeighbours = []
    for i in TempLeaves:
        for j in i.neighbours:
            if j not in TempLeaves and j not in TempNeighbours:
                TempNeighbours.append(j)
    AdjacentEdges = []
    for i in NetworkEdges:
        if (i.u in TempLeaves) ^ (i.v in TempLeaves):
            AdjacentEdges.append(i)
    
    InternalNodes += 1
    InternalNode = Node("InternalNode" + str(InternalNodes), TempNeighbours, "Internal")
    NetworkLeaves.append(InternalNode)
    for i in TempNeighbours:
        for j in i.neighbours:
            if j in TempLeaves:
                i.neighbours.remove(j)
        i.neighbours.append(InternalNode)
    for i in AdjacentEdges:
        if i.u in TempLeaves:
            i.u = InternalNode
        if i.v in TempLeaves:
            i.v = InternalNode
    for i in TempLeaves:
        NetworkLeaves.remove(i)
    for i in Edges:
        NetworkEdges.remove(i)
    
    StemVertexConstructor(InternalNode, newLeaf)

def StemVertexConstructor(node, newLeaf):
    node.neighbours.append(newLeaf)
    NetworkLeaves.append(newLeaf)
    NetworkEdges.append(Edge(node, newLeaf))
    newLeaf.neighbours.append(node)

def ConstructNetwork(NewLeaf):
    weakEdges = []

    for edge in NetworkEdges:
        if edge.type == "StrongEdge":
            print("Strong", NewLeaf.name, edge.name)
            NetworkEdges.remove(edge)
            global InternalNodes
            InternalNodes += 1
            InternalNode = Node("InternalNode"+str(InternalNodes), [edge.u,edge.v,NewLeaf],"Internal")
            NetworkLeaves.append(InternalNode)
            NetworkLeaves.append(NewLeaf)
            NetworkEdges.append(Edge(edge.u,InternalNode))
            NetworkEdges.append(Edge(edge.v,InternalNode))
            NetworkEdges.append(Edge(NewLeaf,InternalNode))

            edge.u.neighbours.remove(edge.v)
            edge.v.neighbours.remove(edge.u)
            edge.u.neighbours.append(InternalNode)
            edge.v.neighbours.append(InternalNode)
            NewLeaf.neighbours.append(InternalNode)
            
            return
        if edge.type == "WeakEdge":
            print('weak', NewLeaf.name, edge.name)
            weakEdges.append(edge)

    if len(weakEdges) != 0:
        WeakEdgeConstructor(weakEdges, NewLeaf)
        return

    constructing = True
    edge = NetworkEdges[0]
    while constructing:
        edge = GetNextEdge(edge)
        if type(edge) is not Edge:
            constructing = False
    StemVertexConstructor(edge, NewLeaf)

        

NetworkLeaves = []
NetworkEdges = []
Leaves = []
Splits = []
InternalNodes = 0

def ConstructTree(file_):
    #Reading the file and constructing a set of leaves and a set of the splits of the network
    with open(file_) as f:
        lines = f.readlines()

    TempLeaves = lines[0].split("(")[1].split(")")[0].split(",")
    for i in TempLeaves:
        Leaves.append(Node(i,[],"Leaf"))

    for i in range(1,len(lines)):
        line = lines[i]
        Splits.append(({line[1],line[3]},{line[5],line[7]}))
        
    #Step 1: Creating the first edge of the network
    Leaves[0].neighbours.append(Leaves[1]), NetworkLeaves.append(Leaves[0])
    Leaves[1].neighbours.append(Leaves[0]), NetworkLeaves.append(Leaves[1])
    NetworkEdges.append(Edge(Leaves[0],Leaves[1]))

    #Step 2: Find stem for next leaf
    length = len(Leaves) - 1
    for i in range(1,length):
        FindStem(Leaves[i+1])
        ConstructNetwork(Leaves[i+1])

    return NetworkLeaves, NetworkEdges
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
