#pip install pillow
#pip install pyzbar
#pip install opencv-python

import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

camera = cv2.VideoCapture(0)
#font = cv2.FONT_HERSHEY_PLAIN

while True:
    _, frame = camera.read()

    qrDecode = pyzbar.decode(frame)
    for i in qrDecode:
        #print("Data", i.data)
        # cv2.putText(frame, str(i.data), (50, 50), font, 2,
        #             (255, 0, 0), 3)
        qrID = i.data
        qrIDs = qrID.decode("utf-8")
        print(qrIDs)

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
