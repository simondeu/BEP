import networkx as nx                   #Networkx library for easy networks             https://networkx.org/
import matplotlib.pyplot as plt         #MatPlotLib library for plotting in python      https://matplotlib.org/
import itertools
import json                             #JSON for storing the graph as a JSON file

def Main(file_, DrawGraph_ = True, StoreGraph_ = True, GraphFile = "graph"):                        #Main file from where the rest of the construction is controlled
    ReadData(file_)                             #Reading the data
    TreeStart()                                 #Start for the blobtree
    for Leaf in G.graph['Leaves'][3::]:         #Loop for adding leaves individually
        CheckEdges(Leaf)                        #Checks for edge types
        AddNextLeaf(Leaf)                       #Adds next leaf according to edge types
    GenerateMixGraph()
    RemoveEdges()
    if DrawGraph_: DrawGraph() 
    if StoreGraph_: StoreGraph(GraphFile)

def ReadData(file_):                    #Function for reading and storing data, data has to be in the format of sample text file
    Leaves = []
    Splits = []

    with open(file_) as f:
        lines = f.readlines()

    TempLeaves = lines[0].split("(")[1].split(")")[0].split(",")
    for i in TempLeaves:
        Leaves.append(i)

    for i in range(1,len(lines)):
        line = lines[i]
        Splits.append(({line[1],line[3]},{line[5],line[7]}))
    
    G.graph['Leaves'], G.graph['Splits'] = Leaves, Splits

def TreeStart():                        #Function for making the base of the tree consisting of 3 leaves and an internal node
    Leaves = G.graph['Leaves']
    StartEdges = [(Leaves[0], "Internal1"), (Leaves[1], "Internal1"), (Leaves[2], "Internal1")]
    G.add_edges_from(StartEdges)
    G.graph["InternalNodes"] = 1

def AddNextLeaf(Leaf):                  #Function for adding the next leaf
    WeakEdges = []
    for edge in G.edges:                        #Iterating over the edges
        u,v = edge[0],edge[1]                   
        if G[u][v]['type'] == "Strong":         #If edge is strong, attach new leaf to edge and repeat process with next leaf
            ConstructStrong(edge,Leaf)          
            return
        if G[u][v]['type'] == "Weak":           #If edge is weak, store it in the weak edges collection
            WeakEdges.append(edge)
    if len(WeakEdges) != 0:                     #If the weak edges collection is not empty, call the function for adding next leaf to the weak edges
        ConstructWeakBlob(WeakEdges, Leaf)
        return
    
    edge = list(G.edges)[0]                     #Starting edge from where we start looking for stem vertex
    constructing = True
    while constructing:                         #Loop for iterating over edges following edge directions
        edge = NextEdge(edge)
        if edge[0] == "Done":                   #If stem vertex is found...
            constructing = False
    ConstructStemVertex(edge[1], Leaf)
    #G.add_edge(Leaf, edge[1])                   #Attach leaf to stem vertex

def NextEdge(edge):                     #Function for getting the next edge for finding the stem vertex
    u,v=edge[0],edge[1]
    direction = G[u][v]['direction']
    for neighbour in G.adj[direction]:
        if G[direction][neighbour]['direction'] is not direction:
            return (neighbour,direction)
    return ("Done",direction)

def CheckEdges(Leaf):                   #Function for getting the type for each edge (Strong, Weak, Directed)
    Splits = G.graph['Splits']
    for edge in G.edges:
        A,B = GetAB(edge[0],edge[1],[]), GetAB(edge[1],edge[0],[])
        Ax,Bx = CheckABx(A,B,Leaf), CheckABx(B,A,Leaf)
        
        if Ax and Bx:
            G[edge[0]][edge[1]]['type'] = "Strong"
        if Ax and not Bx:
            G[edge[0]][edge[1]]['type'] = "Directed"
            G[edge[0]][edge[1]]['direction'] = edge[0]
        if Bx and not Ax:
            G[edge[0]][edge[1]]['type'] = "Directed"
            G[edge[0]][edge[1]]['direction'] = edge[1]
        if not Ax and not Bx:
            G[edge[0]][edge[1]]['type'] = "Weak"

def GetAB(u,v,A=[]):                    #Function for obtaining the sets after a split in the graph
    A.append(u)
    for node in G.adj[u]:
        if node not in A and node is not v:
            A = GetAB(node,u,A)
    return A

def CheckABx(A,B,x):                    #Function for checking if A U {x} is a split with B
    Splits = G.graph['Splits']
    for a in A:
        if "Internal" not in a:
            for b1 in B:
                for b2 in B:
                    if b1 is not b2 and "Internal" not in b1 and "Internal" not in b2:
                        if ({a,x},{b1,b2}) not in Splits and ({b1,b2},{a,x}) not in Splits:
                            return False
    return True

def ConstructStrong(edge, Leaf):        #Function for constructing tree if a strong edge is found, thus attaching the next leaf to the edge
    u,v = edge[0],edge[1]
    G.graph["InternalNodes"] += 1
    NewInternalNode = "Internal"+str(G.graph["InternalNodes"])
    G.remove_edge(u,v)
    G.add_edge(u,NewInternalNode), G.add_edge(v,NewInternalNode), G.add_edge(Leaf,NewInternalNode)

def ConstructWeak(WeakEdges, Leaf):     #Function for constructing the tree with a set of weak edges, merging them to one single vertex and attaching the next leaf to that

    TempNodes = []                                  
    for edge in WeakEdges:                                                          #Making a temporary set of the nodes of the weak edges
        if edge[0] not in TempNodes:
            TempNodes.append(edge[0])
        if edge[1] not in TempNodes:
            TempNodes.append(edge[1])
    
    TempLeaves = []
    for node in TempNodes:                                                          #Making a temporary set of the neighbours attached to the weak edges
        for neighbour in G.adj[node]:
            if neighbour not in TempLeaves and neighbour not in TempNodes:
                TempLeaves.append(neighbour)
    for edge in WeakEdges:                                                          #Removing the weak edges from the graph
        G.remove_edge(edge[0], edge[1])
    for node in TempNodes:
        G.remove_node(node)                                                         #Removing the nodes of the weak edges from the graph
    G.graph["InternalNodes"] += 1
    NewInternalNode = "Internal" + str(G.graph["InternalNodes"])                    #Adding a new internal node
    for node in TempLeaves:                                                         #Attaching the neighbours to the new internal node
        G.add_edge(node,NewInternalNode)
    G.add_edge(Leaf,NewInternalNode)                                                #Attaching the new leaf

def ConstructWeakBlob(WeakEdges, Leaf): #Function for attaching a reticulation vertex to the ends of a weak path, and attaching the next leaf to it
    Ends = []
    TempNodes = []
    for edge in WeakEdges:
        if edge[0] not in Ends:
            Ends.append(edge[0])
        else:
            Ends.remove(edge[0])
        if edge[1] not in Ends:
            Ends.append(edge[1])
        else:
            Ends.remove(edge[1])

        if edge[0] not in TempNodes:
            TempNodes.append(edge[0])
        if edge[1] not in TempNodes:
            TempNodes.append(edge[1])

            
    G.graph["InternalNodes"] += 1
    NewInternalNode = "Internal" + str(G.graph["InternalNodes"])
    if len(Ends) != 0:
        G.add_edges_from([(Ends[0], NewInternalNode, {'reticulation' : (True, NewInternalNode)}),(Ends[1], NewInternalNode, {'reticulation' : (True, NewInternalNode)})]), G.add_edge(NewInternalNode, Leaf)
        return


def ConstructStemVertex(node, Leaf):
    if len(G.adj[node]) <= 3:
        G.add_edge(node, Leaf)
        return
    
    Splits = G.graph['Splits']
    Neighbours = list(G.adj[node])
    RealNeighbours = []
    RealNeighbours+=Neighbours + [Leaf]

    for i, n in enumerate(Neighbours):
        if "Internal" in n:
            y = GetRandomLeafFromInternalNode(n, node, [])
            Neighbours[i] = y

    NeighboursX = Neighbours + [Leaf]
    Neighbours += [Leaf]
    for split in Splits:
        inBlob = True
        for x in split:
            for y in x:
                if y not in NeighboursX:
                    inBlob = False
        if inBlob:
            BlobSplit = split
            for x in split:
                for y in x:
                    if y in NeighboursX:
                        NeighboursX.remove(y)
    G.remove_node(node)
    G.graph["InternalNodes"] += 3
    tempSplit = []
    for x in BlobSplit:
        tmp = []
        for y in x:
            tmp.append(RealNeighbours[Neighbours.index(y)])
        tempSplit.append(tmp)
    NIN1 = "Internal" + str(G.graph["InternalNodes"]-2) 
    NIN2 = "Internal" + str(G.graph["InternalNodes"]-1) 
    NIN3 = "Internal" + str(G.graph["InternalNodes"])
    G.add_edges_from([(tempSplit[0][0], NIN1), (tempSplit[0][1], NIN1), (tempSplit[1][0], NIN2), (tempSplit[1][1], NIN2), (NIN1, NIN2)])
    G.add_edges_from([(NIN1, NIN3, {'reticulation' : (True, NIN3)}), (NIN2, NIN3, {'reticulation' : (True, NIN3)})])
    G.add_edge(NIN3, NeighboursX[0])

def GetRandomLeafFromInternalNode(node, blob, A = []):
    if "Internal" not in node:
        return node
    A.append(blob)
    for x in list(G.adj[node]):
        if x is not blob and x not in A:
            return GetRandomLeafFromInternalNode(x, node, A)

def GenerateMixGraph():                 #Function for converting the graph to a semi-directed graph
    for u,v,data in G.edges(data=True):
        G_mixed.add_edge(u,v,key=0,**data)
        G_mixed.add_edge(v,u,key=0,**data)

def RemoveEdges():                      #Function for removing directed edges that should not be in the graph after the conversion
    EdgesToRemove= []
    for u,v in G_mixed.edges():
        reticulation = G_mixed[u][v][0].get('reticulation',0)
        if reticulation != 0:
            if reticulation[0] == True and reticulation[1] == u:
                EdgesToRemove.append([u,v])
    G_mixed.remove_edges_from(EdgesToRemove)

def DrawGraph():                        #Function that plots the graph
    pos = nx.spring_layout(G_mixed)
    nx.draw(G_mixed, pos, with_labels=False, node_color='lightblue', edge_color='black', node_size=2000, font_size=15)
    labels = {node: str(node) for node in G_mixed.nodes if "Internal" not in node}
    nx.draw_networkx_labels(G_mixed, pos, labels, font_size=12)
    plt.show()

def StoreGraph(GraphFile):              #Function that stores the graph to 'GraphFile.json'
    with open(GraphFile + '.json', 'w') as f:
        json.dump(nx.node_link_data(G_mixed), f, indent=4)

G = nx.Graph()                                                                  #Making a graph object
G_mixed = nx.MultiDiGraph()                                                     #The semi-directed graph we will later convert our graph to
Main("Test.txt", DrawGraph_=True, StoreGraph_=False, GraphFile='graph')         #Calling the main function
