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

def run(ser, slp, hit_distance,velocity, orientation, close_distance, v_decrease):
    """
    ser is the serial object, 
    slp is the sleep time for the qr scan
    hit_distance, distance until an obstacle can be detected
    close_distance, distance approching the wall
    v_decrease, is the percent of decrease of the total velocity for alignment velocity
    """

    # angle between USL and USC has to be measured
    angle = 0.523599
    direction = None
    choice = ''
    dataDict = gtw.read(ser, slp)
    while direction == None:
        dataDict = gtw.read(ser, slp)
        if dataDict['USR'][1] >= hit_distance:
            direction = orientation - angle
            direction = gtw.checkRange(direction)
            choice = 'USR'
        elif dataDict['USL'][1] >= hit_distance:
            direction = orientation + angle
            direction = gtw.checkRange(direction)
            choice = 'USL'
        else:
            gtw.move(ser, (velocity*(-1)), (velocity*(-1)))
    # change orientation to direction orientation
    gtw.alignOrientation(ser, velocity, dataDict['IMU'][-1], direction)
    dataDict = gtw.read(ser, slp)
    # move forward until you are close enough to the object
    while  dataDict[choice][1] > close_distance:
        gtw.move(ser, velocity*v_decrease, velocity*v_decrease)
        dataDict = gtw.read(ser, slp)
    # change orientation to the original orientation he once was
    dataDict = gtw.read(ser, slp)
    gtw.alignOrientation(ser, velocity, dataDict['IMU'][-1], orientation)
    # Check for obstacles, if no obstacles, change to go to waypoint mode
    obstacle = check_obstacle(ser, slp, hit_distance)
    if (obstacle == True):
        return True
    else:  
        return False