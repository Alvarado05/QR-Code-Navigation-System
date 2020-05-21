from go_to_waypoint import go_to_waypoint as gtw
import serial

def run(ser, hit_distance, corr_angle, velocity, tolerance, v_decrease):
    data = gtw.read(ser, 121)
    left = data['USSL'][-1]
    right = data['USSR'][-1]
    hit = True
   
    while hit == True:
        data = gtw.read(ser, 121)
        left = data['USSL'][-1]
        right = data['USSR'][-1]
        changeValue = False

        if left < hit_distance and right > hit_distance:
            final_orientation = data['IMU'][-1] - corr_angle
            final_orientation, changeValue = gtw.checkRange(final_orientation)
            gtw.alignOrientation(ser, velocity, final_orientation, tolerance, v_decrease)
            print("We got a hit in the left")

        elif right < hit_distance and left > hit_distance:
            final_orientation = data['IMU'][-1] + corr_angle
            final_orientation, changeValue = gtw.checkRange(final_orientation)
            gtw.alignOrientation(ser, velocity, final_orientation, tolerance, v_decrease)
            print("We got a hit in the right")

        elif left < hit_distance and right < hit_distance:
            print("hit on both sides")

        else:
            hit = False
            print("No hits")
        
def run2():
    ser = serial.Serial(str('/dev/ttyACM0'), baudrate = 9600, timeout = .1)   # Setup for the arduino communication
    hit_distance = 34
    corr_angle = 0.174533
    velocity = 50
    tolerance = 0.05
    run(ser, hit_distance, corr_angle, velocity, tolerance)