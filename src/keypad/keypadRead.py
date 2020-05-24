from evdev import InputDevice, categorize, ecodes
import sys
import time


device = InputDevice("/dev/input/event3") # my keyboard

event = device.active_keys(verbose=True)

while event == []:
 event = device.active_keys(verbose=True)


device.close()
event = event[0][0].split('KP')
event = event[1]
print(event)
