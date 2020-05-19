# This section of the code will take care of call the required functions to control the robots states
# it also takes care to send the right data in the right formats to the funtcions
from standby import standby
from A_Star import aStar
from general_functions import general_functions as gf
from go_to_waypoint import go_to_waypoint as gtw
import pandas as pd
NODE_FILE = "src/A_Star/Maps/SecondFloorG.csv"
CONNECTION_FILE = "src/A_Star/Maps/SecondFloorConnections.csv"
NORTH = 1.5
DIREC_DICT = gf.northToCardinal(NORTH)
COMPORT = '/dev/ttyACM1'
nodes_df = pd.read_csv(NODE_FILE, index_col='Nodes')
connections_df = pd.read_csv(CONNECTION_FILE)


nodes = standby.run(nodes_df)
while nodes == "Invalid Nodes" or nodes == "Delivered":
    print("Invalid Input")
    print("Please enter start and end nodes")
    nodes = standby.run(nodes_df)
steps = aStar.run(nodes[0], nodes[1], nodes_df, connections_df)
directions = gf.stepsToCardinality(steps, nodes_df)
directions = gf.cardToOrientation(directions,DIREC_DICT)
tolerance = .1
velocity = 50
for direction in directions:
    waypoint = gtw.run(COMPORT, direction, tolerance, velocity)
    print(waypoint)


