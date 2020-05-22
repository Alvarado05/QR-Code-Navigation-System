#print("Data", i.data)
# cv2.putText(frame, str(i.data), (50, 50), font, 2,
#             (255, 0, 0), 3)
#font = cv2.FONT_HERSHEY_PLAIN
# key = cv2.waitKey(1)
# if key == 27:
#   break


#pip install pillow
#pip install pyzbar
#pip install opencv-python

import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

import pyqrcode
from pyzbar.pyzbar import decode
from PIL import Image

camera = cv2.VideoCapture(0)
def qrScanner():
    """This function use the device webcam to scan QR codes, if the function does not detect a QR code returns a "None" value otherwise returns a string of the value in the QR code"""
    j = 0
    qrIDs = ""

    while j < 20:
        _, frame = camera.read()

        gray = cv2.cvtColor(frame[100:250, 240:390], cv2.COLOR_BGR2GRAY)
        qrDecode = pyzbar.decode(gray)
        for i in qrDecode:

            qrID = i.data
            qrIDs = qrID.decode("utf-8")

        # cv2.imshow("Camera", gray)
        j = j + 1

        if qrIDs != "":
            return qrIDs
    return None
            
def qrGenerator(qrValue, qrName):
    """This function receive two string parameters, first one is the value of the wanted QR code and the second one is the name of the QR code image (Example: 'QR.png')"""
    qr = pyqrcode.create(qrValue)
    qr.png(qrName, scale=8)
