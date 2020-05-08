import serial
ser = serial.Serial('com5', 9600)

def getValues():
    ser.write('d')
    arduinoData = ser.readline().decode('ascii')
    return arduinoData

while (1):
    userInput = input('Get data point?')

    if userInput == 'y':
        print(getValues())