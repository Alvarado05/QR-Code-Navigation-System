# This section of the code will take care of call the required functions to control the robots states
# it also takes care to send the right data in the right formats to the funtcions
from standby import standby
from A_Star import aStar
from general_functions import general_functions as gf
from go_to_waypoint import go_to_waypoint as gtw
import pandas as pd
NODE_FILE = "src/A_Star/Maps/CarlosSecondFloor.csv"
CONNECTION_FILE = "src/A_Star/Maps/CarlosSecondFloorConnections.csv"
NORTH =2.06
DIRECT_DICT = gf.northToCardinal(NORTH)
COMPORT = '/dev/ttyACM0'
nodes_df = pd.read_csv(NODE_FILE, index_col='Nodes')
connections_df = pd.read_csv(CONNECTION_FILE)
print(DIRECT_DICT)

nodes = standby.run(nodes_df)
while nodes == "Invalid Nodes" or nodes == "Delivered":
    print("Invalid Input")
    print("Please enter start and end nodes")
    nodes = standby.run(nodes_df)
steps = aStar.run(nodes[0], nodes[1], nodes_df, connections_df)
directions = gf.stepsToCardinality(steps, nodes_df)
directions = gf.cardToOrientation(directions, DIRECT_DICT)
# print(directions)
tolerance = 0.05
velocity = 50
i = len(directions)
i2 = 0
while i2 < i:
    print('i2: ',i2)
    print('steps: ',steps[i2])
    waypoint = gtw.run(COMPORT, directions[i2], tolerance, velocity)
    print("I SAW IT!!!!!!!",waypoint)
    print(directions[i2])
    waypoint = int(waypoint)
    if waypoint == steps[i2]:
        i2 = i2 +1
# print(waypoint)





