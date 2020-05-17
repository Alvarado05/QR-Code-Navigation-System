import serial
import time

ser = serial.Serial('COM5', baudrate = 9600, timeout = 1)


def getSensorInfo():
    while(1):
        ser.write(b'd\n')                    # sending a d with endline to the arduino serial for sensor info
        ser.write(b'v,50,50\n')              # motor commands, v (to activate motor), 50 (left motor velocity), 50 (right motor velocity)
        time.sleep(.01)                      # the frequency of the samples for the sensors to adquiere the info

        arduinoData = ser.read_until("\n").decode('ascii')        # reading the info from arduino and decoding it (ascii)
        print(arduinoData)                                        # priting the arduino serial (sensors info)

  
getSensorInfo();

# def getValues():
    
#     ser.write(b'd')
#     arduinoData = ser.readline().decode('ascii')
#     return arduinoData


# while(1):

#     userInput = input('Get data point?')

#     if userInput == 'y':
#         print(getValues())