import pandas as pd
nodeFile = "Maps/SecondFloorG.csv"
connectionFile = "Maps/SecondFloorConnections.csv"
nodes = pd.read_csv(nodeFile)
connections = pd.read_csv(connectionFile)



def graphMap():
    None

calculateCoordinates(nodes, connections)