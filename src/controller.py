# This section of the code will take care of call the required functions to control the robots states
# it also takes care to send the right data in the right formats to the funtcions
from standby import standby
from A_Star import aStar
from general_functions import general_functions as gf
from go_to_waypoint import go_to_waypoint as gtw
from go_to_waypoint import collision_avoidance as cav
import pandas as pd
NODE_FILE = "src/A_Star/Maps/CarlosSecondFloor.csv"
CONNECTION_FILE = "src/A_Star/Maps/CarlosSecondFloorConnections.csv"
NORTH = 1.99
DIRECT_DICT = gf.northToCardinal(NORTH)
COMPORT = '/dev/ttyACM0'
nodes_df = pd.read_csv(NODE_FILE, index_col='Nodes')
connections_df = pd.read_csv(CONNECTION_FILE)
print(DIRECT_DICT)

# nodes = standby.run(nodes_df)
# while nodes == "Invalid Nodes" or nodes == "Delivered":
#     print("Invalid Input")
#     print("Please enter start and end nodes")
#     nodes = standby.run(nodes_df)
# steps = aStar.run(nodes[0], nodes[1], nodes_df, connections_df)
# directions = gf.stepsToCardinality(steps, nodes_df)
# # print(directions)
# directions = gf.cardToOrientation(directions, DIRECT_DICT)
# # print(directions)
# tolerance = 0.02
# velocity = 50
# print(steps)
# steps.pop(0)
# print(steps)

# gtw.run(COMPORT, directions, steps, tolerance, velocity)

# node = standby.run(nodes_df)

# while node != "Delivered":
#     node = standby.run(nodes_df)

# steps.reverse()
# directions = gf.stepsToCardinality(steps, nodes_df)
# print(directions)
# directions = gf.cardToOrientation(directions, DIRECT_DICT)
# print(directions)
# steps.pop(0)
# print(steps)
# gtw.run(COMPORT, directions, steps, tolerance, velocity)

cav.run2()