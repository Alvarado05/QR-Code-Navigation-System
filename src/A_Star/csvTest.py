import pandas as pd
import aStar


nodeFile = "src/A_Star/Maps/SecondFloorG.csv"
connectionFile = "src/A_Star/Maps/SecondFloorConnections.csv"
connections = pd.read_csv(connectionFile)
nodes = pd.read_csv(nodeFile, index_col = 'Nodes')


print(aStar.run(20,14))
aStar.graphMap(nodes, connections)
