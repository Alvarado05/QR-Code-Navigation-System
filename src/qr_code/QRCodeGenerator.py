#pip install pypng
#pip install pyqrcode

#Generate QR Code
import pyqrcode
from pyzbar.pyzbar import decode
from PIL import Image

qr = pyqrcode.create('hello')
qr.png('qr1.png', scale=8)

url = pyqrcode.create('Test')
url.png('qr2.png', scale=8)
#Read QR Code

# d = decode(Image.open('qr1.png'))

# print(d[0].data.decode('ascii'))
