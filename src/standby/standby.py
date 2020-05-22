import pandas as pd
from general_functions import general_functions as gf
import time
def run(nodes, keypad):
    nodes = nodes.index.tolist()
    print(nodes)
    while True:
        missionNodes = []
        inNodes = False
        inNodes2 = False
        if keypad == True:
            startNode = gf.keypadRead()
            time.sleep(1)
        else:
            startNode = input()


        try:
            startNode = int(startNode)
        except:
            None

        if startNode == "*":
            return "Delivered"
        else:

            if keypad == True:
                endNode = gf.keypadRead()
                time.sleep(1)
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
