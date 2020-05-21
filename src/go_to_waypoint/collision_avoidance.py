import go_to_waypoint as gtw
import serial

ser = serial.Serial(str('/dev/ttyACM0'), baudrate = 9600, timeout = .1)   # Setup for the arduino communication
def run(ser):
    data = gtw.read(ser, 121)


    print(data['USSL'][-1])
    print(data['USSR'][-1])

run(ser)