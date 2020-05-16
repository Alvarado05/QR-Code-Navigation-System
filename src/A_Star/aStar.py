import pandas as pd
import math

def heuristicCalc(nodes, endNode):
    """
    Returns nodes df with a new column ("Distance with (endNode)") that contain
    The distances of all nodes to endNode

    Accepts as Input:
    
    nodes: dataframe with the nodes as index names and X,Y as columns
    
    endNode: the node that the function will use as reference
    """
    endCoor = nodes.loc[endNode, :].tolist()
    nodes_sub = [(nodes['X'] - endCoor[0]).values.tolist(), (nodes['Y'] - endCoor[1]).values.tolist()]
    nodes_sub = [[nodes_sub[0][i], nodes_sub[1][i] ]for i in range(len(nodes_sub[0]))]
    distance = [math.hypot(sub[0], sub[1])for sub in nodes_sub]
    dist = "Distance with " + str(endNode)
    nodes[dist] = distance
    return nodes

def aStarCalc(startNode, endNode, nodes, connections):
    """
    Returns a list with the nodes that the algorithm passed to go from the start node to de end node.

    Accepts as Inputs:
    
    startNode: A string that contains the name of the start node.
    
    endNode: A string that contains the name of the end node.
    
    nodes: A dataframe with the nodes as index names and X,Y as columns
    
    connections: A datafrmae with the connection between two nodes in two columns
    """
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
    """
    Returns a list that contains the best path from the start node to the end node.

    Accepts as Input:
    
    endNode: A string that contains the name of the end node.
    
    steps: A list with the nodes that the algorithm passed to go from the start node to de end node.
    
    connections: A dataframe with the connection between two nodes in two columns
    """
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

def run(startNode, endNode, nodes, connections):
    """
    Returns a list that contains the best path from the start node to the end node.

    Accepts as Inputs:
    
    startNode: A string that contains the name of the start node.
    
    endNode: A string that contains the name of the end node.

    connections: A dataframe with the connection between two nodes in two columns

    nodes: A dataframe with the nodes as index names and X,Y as columns
    """
    nodes = heuristicCalc(nodes, endNode)
    nodes.columns =  ['X', 'Y', 'H']
    nodes = heuristicCalc(nodes, startNode)
    nodes.columns = ['X', 'Y', 'H', 'G']
    nodes['F'] = nodes['H'] + nodes['G']
    steps = aStarCalc(startNode, endNode, nodes, connections)
    steps = stepCleanup(steps,endNode,connections)
    return steps
