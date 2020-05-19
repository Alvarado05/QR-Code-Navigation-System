import pandas as pd

def run(nodes):
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
