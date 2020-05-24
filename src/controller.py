# This section of the code will take care of call the required functions to control the robots states
# it also takes care to send the right data in the right formats to the funtcions
from standby import standby
from A_Star import aStar
from general_functions import general_functions as gf
from go_to_waypoint import go_to_waypoint as gtw
from go_to_waypoint import collision_avoidance as cav
import pandas as pd
import serial
NODE_FILE = "src/A_Star/Maps/CarlosSecondFloor.csv"
CONNECTION_FILE = "src/A_Star/Maps/CarlosSecondFloorConnections.csv"
NORTH = 2.35
DIRECT_DICT = gf.northToCardinal(NORTH)
COMPORT = '/dev/ttyACM0'
KEYPAD = True
ser = serial.Serial(str(COMPORT), baudrate = 9600, timeout = .1)   # Setup for the arduino communication

nodes_df = pd.read_csv(NODE_FILE, index_col='Nodes')
connections_df = pd.read_csv(CONNECTION_FILE)
print(DIRECT_DICT)

nodes = standby.run(nodes_df, KEYPAD)
while nodes == "Invalid Nodes" or nodes == "Delivered":
    print("Invalid Input")
    print("Please enter start and end nodes")
    gtw.buzzer(ser,-1)
    nodes = standby.run(nodes_df, KEYPAD)
steps = aStar.run(nodes[0], nodes[1], nodes_df, connections_df)
directions = gf.stepsToCardinality(steps, nodes_df)
# print(directions)
directions = gf.cardToOrientation(directions, DIRECT_DICT)
# print(directions)
tolerance = 0.07
velocity = 50
v_decrease = .80
print(steps)
steps.pop(0)
print(steps)

gtw.run(ser, directions, steps, tolerance, velocity, v_decrease)
gtw.buzzer(ser, 0)
node = standby.run(nodes_df, KEYPAD)

while node != "Delivered":
    gtw.buzzer(ser,-1)
    node = standby.run(nodes_df, KEYPAD)


steps.reverse()
directions = gf.stepsToCardinality(steps, nodes_df)
print(directions)
directions = gf.cardToOrientation(directions, DIRECT_DICT)
print(directions)
steps.pop(0)
print(steps)
gtw.run(ser, directions, steps, tolerance, velocity, v_decrease)

