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

def check_obstacle(ser, slp, hit_distance):
    dataDict = gtw.read(ser, slp)
    if dataDict['USC'][1] < hit_distance:
        return True
    else:
        return False

def run(ser, slp, hit_distance,velocity, orientation):
    # angle between USL and USC has to be measured
    angle = 0.523599
    direction = ''
    dataDict = gtw.read(ser, slp)
    while direction == '':
        dataDict = gtw.read(ser, slp)
        if dataDict['USR'][1] >= hit_distance:
            direction = orientation - angle
        elif dataDict['USL'][1] >= hit_distance:
            direction = 'L'
        else:
            gtw.move(ser, (velocity*(-1)), (velocity*(-1)))
    
    if direction == 'R':
        None
        #move angle to the right
    if direction == 'L':
        None
        #move angle to the left