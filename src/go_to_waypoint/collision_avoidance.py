from go_to_waypoint import read as gtw
import serial

ser = serial.Serial(str('/dev/ttyACM0'), baudrate = 9600, timeout = .1)   # Setup for the arduino communication
def run(ser, hit_distance):
    data = gtw.read(ser, 121)


    print(data['USSL'][-1])
    print(data['USSR'][-1])
    left = data['USSL'][-1]
    right = data['USSR'][-1]
    if left < hit_distance and right > hit_distance:
        print("We got a hit in the left")
    elif right < hit_distance and left > hit_distance:
        print("We got a hit in the right")
    else:
        print("hit to both sides")

run(ser)