'''
USL = Ultra Sonic Left
USR = Ultra Sonic Right
USC = Ultra Sonic Center
If USC = 55cm for the first hit 2 tiles
'''

import go_to_waypoint as gtw
#Pop the keys GRF,GRW,IMU and ODOM.
#Once you only have USL,USC and USR check if USC is equal to 55.
#Stop the rover.

def check_obstacle(ser, slp):
    hit_distance = 55
    dataDict = gtw.read(ser, slp)
    if dataDict['USC'][1] > hit_distance:
        return True

def run():
    hit_distance = 55
    print()
    None

