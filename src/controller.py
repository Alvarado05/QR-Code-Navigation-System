# This section of the code will take care of call the required functions to control the robots states
# it also takes care to send the right data in the right formats to the funtcions
from standby import standby
from A_Star import aStar
from general_functions import general_functions as gf
import pandas as pd
NODE_FILE = "src/A_Star/Maps/SecondFloorG.csv"
CONNECTION_FILE = "src/A_Star/Maps/SecondFloorConnections.csv"
DIREC_DICT ={'N': 90, 'S': 270, 'E':0, 'W': 180}
nodes_df = pd.read_csv(NODE_FILE, index_col='Nodes')
connections_df = pd.read_csv(CONNECTION_FILE)


nodes = standby.standBy(nodes_df)
while nodes == "Invalid Nodes" or nodes == "Delivered":
    print("Invalid Input")
    print("Please enter start and end nodes")
    nodes = standby.standBy(nodes_df)
steps = aStar.run(nodes[0], nodes[1], nodes_df, connections_df)
directions = gf.stepsToCardinality(steps, nodes_df)
directions = gf.cardToOrientation(directions,DIREC_DICT)


