import pandas as pd
import math
import networkx as nx
import matplotlib.pyplot as plt

def heuristicCalc(nodes, endNode):
    """
    Returns nodes df with a new column ("Distance with (endNode)") that contain
    The distances of all nodes to endNode

    Accepts as Input:
    nodes: df with the nodes as index names and X,Y as columns
    endNode: the node that the function will use as reference
    """
    endCoor = nodes.loc[endNode, :].tolist()
    nodes_sub = [(nodes['X'] - endCoor[0]).values.tolist(), (nodes['Y'] - endCoor[1]).values.tolist()]
    nodes_sub = [[nodes_sub[0][i], nodes_sub[1][i] ]for i in range(len(nodes_sub[0]))]
    distance = [math.hypot(sub[0], sub[1])for sub in nodes_sub]
    dist = "Distance with " + endNode
    nodes[dist] = distance
    return nodes
    
def graphMap(nodes, connections):
    grafo = nx.Graph()
    fig, ax = plt.subplots()

    #print(nodes.iloc[0,:])
    grafo.add_node("A", pos=(1, 11))
    grafo.add_node("B", pos=(4, 11))
    grafo.add_node("C", pos=(16, 11))
    grafo.add_node("D", pos=(1, 7))
    grafo.add_node("E", pos=(4, 7))
    grafo.add_node("F", pos=(13, 7))
    grafo.add_node("G", pos=(19, 7))
    grafo.add_node("H", pos=(1, 5))
    grafo.add_node("I", pos=(4, 5))
    grafo.add_node("J", pos=(16, 5))
    grafo.add_node("K", pos=(19, 5))
    grafo.add_node("L", pos=(4, 1))
    grafo.add_node("M", pos=(13, 1))
    grafo.add_node("N", pos=(19, 1))
    grafo.add_node("a", pos=(1, 9))
    grafo.add_node("b", pos=(4, 9))
    grafo.add_node("c", pos=(7, 9))
    grafo.add_node("d", pos=(10, 9))
    grafo.add_node("e", pos=(13, 9))
    grafo.add_node("f", pos=(16, 9))
    grafo.add_node("g", pos=(19, 9))
    grafo.add_node("h", pos=(1, 3))
    grafo.add_node("i", pos=(4, 3))
    grafo.add_node("j", pos=(7, 3))
    grafo.add_node("k", pos=(10, 3))
    grafo.add_node("l", pos=(13, 3))
    grafo.add_node("m", pos=(16, 3))
    grafo.add_node("n", pos=(19, 3))

    grafo.add_edge("A", "a")
    grafo.add_edge("B", "b")
    grafo.add_edge("C", "f")
    grafo.add_edge("D", "a")
    grafo.add_edge("E", "b")
    grafo.add_edge("F", "e")
    grafo.add_edge("G", "g")
    grafo.add_edge("H", "h")
    grafo.add_edge("I", "i")
    grafo.add_edge("J", "m")
    grafo.add_edge("K", "n")
    grafo.add_edge("L", "i")
    grafo.add_edge("M", "l")
    grafo.add_edge("N", "n")
    grafo.add_edge("a", "b")
    grafo.add_edge("b", "c")
    grafo.add_edge("c", "d")
    grafo.add_edge("c", "j")
    grafo.add_edge("d", "k")
    grafo.add_edge("d", "e")
    grafo.add_edge("e", "f")
    grafo.add_edge("g", "f")
    grafo.add_edge("h", "i")
    grafo.add_edge("i", "j")
    grafo.add_edge("L", "i")
    grafo.add_edge("j", "k")
    grafo.add_edge("k", "l")
    grafo.add_edge("l", "m")
    grafo.add_edge("m", "n")

    pos = nx.get_node_attributes(grafo, 'pos')

    nx.draw(grafo, pos, with_labels=True)
    limits = plt.axis('on')
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.show()

def aStarCalc(startNode, endNode, nodes, connections):
    openNodes = [startNode]
    closedNodes = []
    steps =[]
    endReached = False
    while not endReached:
        current = nodes.loc[openNodes, :]['F'].idxmin()
        steps.append(current)
        openNodes.remove(current)
        closedNodes.append(current)
        if current == endNode:
            break
        for neighbor in connections.loc[connections['Node2'] == current, 'Node1'].values.tolist():
            # print("OpenNodes: ")
            # print(openNodes)
            # print("Neighbor of " + current + " is: " + neighbor)
            try:
                closedNodes.index(neighbor)
                continue
            except:
                None
            try:
                openNodes.index(neighbor)
            except:
                openNodes.append(neighbor)
    return steps

def stepCleanup(steps, endNode, connections):
    steps.reverse()
    newSteps =[]
    for i in range(len(steps)):
        if steps[i] == endNode:
            newSteps.append(steps[i])
            continue
        
        # if steps[i] is in neighbors of steps[i-1], add to new steps, do nothing

        for neighbor in connections.loc[connections['Node2'] == newSteps[-1], 'Node1'].values.tolist():
            # print(steps[i-1])
            # print(neighbor)
            if neighbor == steps[i]:
                newSteps.append(steps[i])
                break
    newSteps.reverse()
    return newSteps

def run(startNode, endNode):
    nodeFile = "src/A_Star/Maps/SecondFloorG.csv"
    connectionFile = "src/A_Star/Maps/SecondFloorConnections.csv"
    connections = pd.read_csv(connectionFile)
    nodes = pd.read_csv(nodeFile, index_col = 'Nodes')


    nodes = heuristicCalc(nodes, endNode)
    nodes.columns =  ['X', 'Y', 'H']
    nodes = heuristicCalc(nodes, startNode)
    nodes.columns = ['X', 'Y', 'H', 'G']
    nodes['F'] = nodes['H'] + nodes['G']
    steps = aStarCalc(startNode, endNode, nodes, connections)
    steps = stepCleanup(steps,endNode,connections)
    return steps

test = run('A', 'N')
print(test)
    











