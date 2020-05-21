from evdev import InputDevice, categorize, ecodes

device = InputDevice("/dev/input/event6") # my keyboard
for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        print(categorize(event))
