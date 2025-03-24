# from lock_controller import countItDown, lockState
# from isDoorClosed import isDoorClosed
# from rest_endpoint import runApi
# from threading import Thread

# t1 = Thread(target=countItDown)
# t2 = Thread(target=lockState)
# t3 = Thread(target=isDoorClosed)
# # t4 = Thread(target=runApi)
# t1.start()
# t2.start()
# t3.start()
# # t4.start()


# from py122u import nfc

# reader = nfc.Reader()
# reader.connect()
# reader.print_data(reader.get_uid())
# reader.info()

# import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522

# reader = SimpleMFRC522()


# id, text = reader.read()
# print(id)
# print(text)

# GPIO.cleanup()
# from lcd_controller import changeState


# input()
# changeState()

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()


print("Waiting for an ID...")
cardData = reader.read_id()
cardDataInHex = f"{cardData:x}"
minusMfgID = cardDataInHex[:-2]
big_endian = bytearray.fromhex(str(minusMfgID))
big_endian.reverse()
little_endian = "".join(f"{n:02X}" for n in big_endian)
print(
    "User ID "
    + str(cardData)
    + " scanned and converted to little endian ID of: "
    + str(minusMfgID)
)