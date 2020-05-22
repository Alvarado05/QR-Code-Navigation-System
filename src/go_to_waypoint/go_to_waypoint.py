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
from go_to_waypoint import collision_avoidance as cav
import math

def move(ser, leftV, rightV):
    print("LeftV:", leftV)
    print("rightV:", rightV)
    concatenation = 'v,'+ str(leftV) + ',' + str(rightV) +'\n'
    print(concatenation)
    ser.write(bytes(concatenation, 'ascii')) 

def stop(ser):
    ser.write(b's\n')
def read(ser, slp):
    ser.write(b'd\n')
    # time.sleep(slp)
    splitedList = []                                        # the frequency of the samples for the sensors to adquiere the info
    arduinoData = ser.read_until("\n").decode('ascii')      # reading the info from arduino and decoding it (ascii)
    arduinoData = arduinoData.splitlines()
    
    for i in range(len(arduinoData)):
            splitedList.append(arduinoData[i].split(','))   # priting the arduino serial (sensors info)
    print(splitedList)
    dataDict = {j[0]:[float(i) for i in j[1:]]  for j in splitedList}
    return dataDict                                         # priting the arduino serial (sensors info)

def checkRange(degree):
    changeValue = False
    if degree  < 0:
        degree = degree + (2*math.pi)
        print("changed Value")
        changeValue = True
    elif degree > (2 * math.pi):
        degree = degree - (2*math.pi)
        print("changed Value")
        changeValue = True
    return degree , changeValue

def changeOrientation(ser, velocity, start_orientation, final_orientation):
    angle_between = start_orientation-final_orientation
    if angle_between < 0:
        angle_between = angle_between + 2*math.pi
    if angle_between <= math.pi:
        move(ser, velocity,velocity*(-1))
    elif angle_between > math.pi:
        move(ser,velocity*(-1),velocity)
    return None

def alignOrientation (ser, velocity, final_orientation, tolerance, v_decrease):
    # while orientation is not right, rotate
    min_orientation = final_orientation - tolerance
    max_orientation = final_orientation + tolerance

    changeValue = False
    # if any of the two fall outside the rango of 0-360, convert them
    min_orientation, changeValue = checkRange(min_orientation)
    max_orientation, changeValue = checkRange(max_orientation)
    print("The minimum orientation is:", min_orientation)
    print("The maximum orientation is:", max_orientation)

    data = read(ser, .0001)
    cur_orientation = data['IMU'][-1]
    
    if changeValue == False:
        while (cur_orientation <= (min_orientation) or cur_orientation >= (max_orientation)):
            data = read(ser, .0001)
            cur_orientation = data['IMU'][-1]
            print("Aligning from:", cur_orientation, "to:", final_orientation)
            changeOrientation(ser, velocity, cur_orientation, final_orientation)
            data = read(ser, .0001)
            cur_orientation = data['IMU'][-1]
            print("changeValue:", changeValue)
            print(cur_orientation)
    else: 
        while (cur_orientation > max_orientation and cur_orientation < min_orientation):
            data = read(ser, .0001)
            cur_orientation = data['IMU'][-1]
            changeOrientation(ser, velocity, cur_orientation, final_orientation) 
            data = read(ser, .0001)
            cur_orientation = data['IMU'][-1]
            print("changeValue:", changeValue)          
            print(cur_orientation)
    print('Finished Rotation')        
    stop(ser)

def run(comChannel, orientations, steps, tolerance, velocity, v_decrease):
    ser = serial.Serial(str(comChannel), baudrate = 9600, timeout = .1)   # Setup for the arduino communication
    i = len(orientations)
    i2 = 0
    hit_distance = 24
    front_hit_distance = 40
    corr_angle = 0.174533
    while i2 < i :

        print("Orientation:", orientations[i2])
        print("Step:", steps[i2])
        

        alignOrientation(ser, velocity, orientations[i2], tolerance, v_decrease)

        scan = qrf.qrScanner()                              # scan qrCode
        
        while scan == None or scan != steps[i2]:                                 # while qrcode not present
            cav.run(ser, hit_distance, front_hit_distance, corr_angle, velocity, tolerance, v_decrease)
            move(ser,velocity, velocity)                    #   Move forward
            print("Scanning")
            scan = qrf.qrScanner()                          #   scan qrCode
            if scan != None:
                scan = int(scan)
        stop(ser)                                           # stop
        i2 = i2 + 1
   
    return None


