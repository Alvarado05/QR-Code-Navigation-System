from go_to_waypoint import go_to_waypoint as gtw
import serial

def run(ser, hit_distance, front_hit_distance,  corr_angle, velocity, tolerance, v_decrease):
    data = gtw.read(ser, 121)
    side_left = data['USSL'][-1]
    side_right = data['USSR'][-1]
    center = data['USC'][-1]
    left = data['USL'][-1]
    right = data['USR'][-1]

    if (left < front_hit_distance and right > front_hit_distance):
        print("We got a hit in the front left")
        final_orientation = data['IMU'][-1] - 0.349066
        final_orientation, changeValue = gtw.checkRange(final_orientation)
        gtw.alignOrientation(ser, velocity, final_orientation, tolerance, v_decrease)
    elif (right < front_hit_distance and left > front_hit_distance):
        print("We got a hit in  front right")
        final_orientation = data['IMU'][-1] + 0.349066
        final_orientation, changeValue = gtw.checkRange(final_orientation)
        gtw.alignOrientation(ser, velocity, final_orientation, tolerance, v_decrease)

    elif (side_left < hit_distance and side_right > hit_distance):
        print("We got a hit in the left")
        final_orientation = data['IMU'][-1] - corr_angle
        final_orientation, changeValue = gtw.checkRange(final_orientation)
        gtw.alignOrientation(ser, velocity, final_orientation, tolerance, v_decrease)
        

    elif (side_right < hit_distance and side_left > hit_distance):
        print("We got a hit in the right")
        final_orientation = data['IMU'][-1] + corr_angle
        final_orientation, changeValue = gtw.checkRange(final_orientation)
        gtw.alignOrientation(ser, velocity, final_orientation, tolerance, v_decrease)
        
    elif side_left < hit_distance and side_right < hit_distance:
        print("hit on both sides")
        
    elif center < hit_distance:
        print("hit on the front")
        
    else:
        print("No hits")
        
# def run2():
#     ser = serial.Serial(str('/dev/ttyACM0'), baudrate = 9600, timeout = .1)   # Setup for the arduino communication
#     hit_distance = 35
#     front_hit_distance = 45
#     v_decrease = .80
#     corr_angle = 0.122173
#     velocity = 50
#     tolerance = 0.07
#     run(ser, hit_distance, front_hit_distance, corr_angle, velocity, tolerance, v_decrease)