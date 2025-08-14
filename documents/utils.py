# documents/utils.py
import qrcode

def generer_qr_code(data):
    qr = qrcode.make(data)
    qr.save("media/qrcodes/qr_code.png")
