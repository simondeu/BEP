import BlobTreeConstructor as BTC
import DrawNetwork as DN

NetworkNodes, NetworkEdges = BTC.ConstructTree("Test.txt")
DN.DrawNetwork(NetworkNodes, NetworkEdges)
