import pandas as pd
nodeFile = "src/A_Star/Maps/SecondFloorG.csv"
connectionFile = "src/A_Star/Maps/SecondFloorConnections.csv"

connections = pd.read_csv(connectionFile)

nodes = pd.read_csv(nodeFile)
print(nodes.loc[:,'X'])
print(nodes)
print(connections)

def graphMap():
    None
