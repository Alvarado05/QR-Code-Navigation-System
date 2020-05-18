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
    ser.write(b'v,'+ str(leftV) + ',' + str(rightV) +'\n') 
    
def read(ser, slp):
    ser.write(b'd\n')
    time.sleep(slp)
    splitedList = []                                        # the frequency of the samples for the sensors to adquiere the info
    arduinoData = ser.read_until("\n").decode('ascii')      # reading the info from arduino and decoding it (ascii)
    arduinoData = arduinoData.splitlines()
    for i in range(len(arduinoData)):
            splitedList.append(arduinoData[i].split(','))   # priting the arduino serial (sensors info)
    dataDict = {j[0]:j[1:] for j in splitedList}
    return dataDict                                         # priting the arduino serial (sensors info)


def run(comChannel, orientation, tolerance, velocity):

    ser = serial.Serial(str(comChannel), baudrate = 9600, timeout = 1)   # Setup for the arduino communication
    data = read(ser, .01)
    cur_orientation = data['IMU'][-1]

    # while orientation is not right, rotate
    while cur_orientation <= (orientation - tolerance) or cur_orientation >= (orientation + tolerance):
        angle_between = cur_orientation-orientation
        if angle_between < 0:
            angle_between += 2*math.pi
        if angle_between <= math.pi:
            move(ser, velocity*-1,velocity)
        elif angle_between > math.pi:
            move(ser,velocity,velocity*-1)
    move(ser,0,0)
    time.sleep(20)
    
    scan = qrf.qrScanner()                              # scan qrCode
    while scan == None:                                 # while qrcode not present
        move(ser,velocity, velocity)                    #   Move forward
        scan = qrf.qrScanner()                          #   scan qrCode
    move(ser,0, 0)                         # stop
    return scan


