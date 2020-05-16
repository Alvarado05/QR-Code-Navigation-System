# This section of the code will take care of call the required functions to control the robots states
# it also takes care to send the right data in the right formats to the funtcions
from standby import standby
from A_Star import aStar
import pandas as pd
NODE_FILE = "src/A_Star/Maps/SecondFloorG.csv"
CONNECTION_FILE = "src/A_Star/Maps/SecondFloorConnections.csv"
nodes_df = pd.read_csv(NODE_FILE, index_col='Nodes')
connections_df = pd.read_csv(CONNECTION_FILE)


print(connections_df)
nodes = standby.standBy(nodes_df)
while nodes == "Invalid Nodes":
    print("Invalid Nodes")
    nodes = standby.standBy(nodes_df)
steps = aStar.run(nodes[0], nodes[1], nodes_df, connections_df)


