# have rover orientate to right orientation
# go forward
# scan for checkpoint
# checkpoint logic  
#   if no checkpoint keep moving forward
#   if checkpoint is the expected checkpoint, stop, return to controller
# # What does it mean? Should I go to the next one?
# obstacle detection    !
# obsatcle logic    !
# determine if path is blocked  !
import serial       # pip install serial, pip install pyserial
import time
from qr_code import QRCodeFunctions as qrf
import math
import obstacle_avoidance as oa

def move(ser, leftV, rightV):
    concatenation = 'v,'+ str(leftV) + ',' + str(rightV) +'\n'
    ser.write(bytes(concatenation, 'ascii')) 

def stop(ser):
    ser.write(b's\n')
def read(ser, slp):
    ser.write(b'd\n')
    time.sleep(slp)
    splitedList = []                                        # the frequency of the samples for the sensors to adquiere the info
    arduinoData = ser.read_until("\n").decode('ascii')      # reading the info from arduino and decoding it (ascii)
    arduinoData = arduinoData.splitlines()
    for i in range(len(arduinoData)):
            splitedList.append(arduinoData[i].split(','))   # priting the arduino serial (sensors info)
    print(splitedList)
    dataDict = {j[0]:[float(i) for i in j[1:]]  for j in splitedList}
    return dataDict                                         # priting the arduino serial (sensors info)

def alignOrientation(ser, velocity, start_orientation, final_orientation):
    angle_between = start_orientation-final_orientation
    if angle_between < 0:
        angle_between += 2*math.pi
    if angle_between <= math.pi:
        move(ser, velocity,velocity*(-1))
    elif angle_between > math.pi:
        move(ser,velocity*(-1),velocity)
    return None

def checkRange(degree):
    if degree  < 0:
        degree = degree + (2*math.pi)
    elif degree > (2 * math.pi):
        degree = degree - (2*math.pi)

    return degree


def run(comChannel, orientation, tolerance, velocity):
    sleep_time = .01
    ser = serial.Serial(str(comChannel), baudrate = 9600, timeout = 1)   # Setup for the arduino communication
    data = read(ser, sleep_time)
    min_orientation = orientation - tolerance
    max_orientation = orientation + tolerance
    
    change_value = False
    # if any of the two fall outside the rango of 0-360, convert them
    min_orientation2 = checkRange(min_orientation)
    max_orientation2 = checkRange(max_orientation)

    if(min_orientation2 != min_orientation2 or max_orientation != max_orientation2):
        change_value = True
        min_orientation = min_orientation2
        max_orientation = max_orientation2
    
    cur_orientation = data['IMU'][-1]

    # while orientation is not right, rotate
    while ((cur_orientation <= (min_orientation) or cur_orientation >= (max_orientation)) and not changeValue) or (changeValue and (cur_orientation > max_orientation and cur_orientation < min_orientation)):
        alignOrientation(ser, velocity, cur_orientation, orientation)
        data = read(ser, sleep_time)
        cur_orientation = data['IMU'][-1]
        print(cur_orientation)
    
    stop(ser)
    
    scan = qrf.qrScanner()                              # scan qrCode
    while scan == None:                                 # while qrcode not present
        checkObs = oa.check_obstacle(ser, sleep_time)
        if checkObs == False:
            move(ser,velocity, velocity)                    #   Move forward
            scan = qrf.qrScanner()                          #   scan qrCode
        elif checkObs == True:
            stop(ser)
            # Obs avoidance
    stop(ser)                                           # stop
    
    return scan


