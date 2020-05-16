import pandas as pd

def standBy(nodes):
    """
    Returns a list with the start node and the end node after the user enter a existent start node end end node. If the user enter a "*", the function will return a delivery confirmation

    Accepts as inputs:

    nodes: A dataframe with the nodes as index names and X,Y as columns
    """
    nodes = nodes.index.tolist()
    print(nodes)
    while True:
        missionNodes = []
        inNodes = False
        inNodes2 = False
        startNode = input()
        try:
            startNode = int(startNode)
        except:
            None

        if startNode == "*":
            return "Delivered"
        else:
            endNode = input()
            try:
                endNode = int(endNode)
            except:
                None

            for i in range(len(nodes)):
                if nodes[i] == startNode:
                    inNodes = True
                if nodes[i] == endNode:
                    inNodes2 = True
            if inNodes == True and inNodes2 == True:
                missionNodes.append(startNode)
                missionNodes.append(endNode)
                return missionNodes
            else:
                return "Invalid Nodes"
