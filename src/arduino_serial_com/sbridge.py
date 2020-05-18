import serial       # pip install serial, pip install pyserial
import time

ser = serial.Serial('/dev/ttyACM0', baudrate = 9600, timeout = 1)   # Setup for the arduino communication


def getSensorInfo():
        ser.write(b'd\n')                    # sending a d with endline to the arduino serial for sensor info
        ser.write(b'v,50,0\n')              # motor commands, v (to activate motor), 50 (left motor velocity), 50 (right motor velocity)
        time.sleep(.1)                      # the frequency of the samples for the sensors to adquiere the info
        splited = []
        arduinoData = ser.read_until("\n").decode('ascii')        # reading the info from arduino and decoding it (ascii)
        arduinoData = arduinoData.splitlines()
        for i in range(len(arduinoData)):
                splited.append(arduinoData[i].split(','))
        dicti = {j[0]:j[1:] for j in splited}
        print(dicti)
  
getSensorInfo()

# def getValues():
    
#     ser.write(b'd')
#     arduinoData = ser.readline().decode('ascii')
#     return arduinoData


# while(1):

#     userInput = input('Get data point?')

#     if userInput == 'y':
#         print(getValues())
