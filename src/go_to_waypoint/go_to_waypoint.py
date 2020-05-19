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

def run(comChannel, orientation, tolerance, velocity):

    ser = serial.Serial(str(comChannel), baudrate = 9600, timeout = 1)   # Setup for the arduino communication
    data = read(ser, .01)
    min_orientation = orientation - tolerance
    max_orientation = orientation + tolerance
    
    changeValue = False
    # if any of the two fall outside the rango of 0-360, convert them
    if min_orientation  < 0:
        min_orientation = min_orientation + (2*math.pi)
        changeValue = True
    elif max_orientation > 360:
        max_orientation = max_orientation - (2*math.pi)
        changeValue = True
    
    cur_orientation = data['IMU'][-1]
    print(data)

    # while orientation is not right, rotate
    while ((cur_orientation <= (min_orientation) or cur_orientation >= (max_orientation)) and not changeValue) or (changeValue and (cur_orientation > max_orientation and cur_orientation < min_orientation)):
        alignOrientation(ser, velocity, cur_orientation, orientation)
        data = read(ser, .01)
        cur_orientation = data['IMU'][-1]
    
    stop(ser)
    
    scan = qrf.qrScanner()                              # scan qrCode
    while scan == None:                                 # while qrcode not present
        move(ser,velocity, velocity)                    #   Move forward
        scan = qrf.qrScanner()                          #   scan qrCode
    stop(ser)                                           # stop
    return scan


