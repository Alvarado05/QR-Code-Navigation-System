from evdev import InputDevice, categorize, ecodes

device = InputDevice("/dev/input/event3") # my keyboard
for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        print(categorize(event))
        print(type(event))
        event = str(categorize(event))
        event = event.split(',')
        event = event[1].split('KP')
        event = event[1]
        event = event[:-1]
        print(event)

