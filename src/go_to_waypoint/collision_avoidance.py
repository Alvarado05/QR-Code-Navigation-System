from go_to_waypoint import go_to_waypoint as gtw
import serial

def run(ser, hit_distance):
    data = gtw.read(ser, 121)
    print(data)
    print(data['USSL'][-1])
    print(data['USSR'][-1])
    left = data['USSL'][-1]
    right = data['USSR'][-1]
    if left < hit_distance and right > hit_distance:
        print("We got a hit in the left")
    elif right < hit_distance and left > hit_distance:
        print("We got a hit in the right")
    elif left < hit_distance and right < hit_distance:
        print("hit on both sides")
    else:
        print("No hits")
def run2():
    ser = serial.Serial(str('/dev/ttyACM0'), baudrate = 9600, timeout = .1)   # Setup for the arduino communication
    hit_distance = 34
    run(ser, hit_distance)