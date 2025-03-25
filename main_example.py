from lcd_controller import lcdScreenController, set_active_state
from threading import Thread
from matrix_driver import keypad
from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from gpiozero import Buzzer

kp = keypad()
buzzer = Buzzer(26)
reader = SimpleMFRC522()
uid_test = "73de2a29"
BASE_API_URL = "keycabinet.cspc.edu.ph/api/"

key = 0
def digit():
    # Loop while waiting for a keypress
    r = None
    while r is None:
        r = kp.getKey()
        sleep(.2) # Wait before checking the keypad again
    return r

def main():
    global key
    while True:
        set_active_state("defaultState")
        key = digit()
        buzzer.on()
        sleep(0.05)
        buzzer.off()
        print(key)
        if key == 1:
            key = None
            displayMain()
            pass
        else:
            print('Invalid key')
            continue  # Exit the loop if 0 is pressed

def displayMain():
    set_active_state("displayMainMenu")
    global key
    while True:
        key = digit()
        while key is None:
            buzzer.off()
        buzzer.on()
        sleep(0.05)
        buzzer.off()
        if key == 0:
            key = None
            return  # Exit to the previous menu
        elif key == 1:
            key = None
            selectKey()
            return
        elif key == 2:
            key = None
            scanID()
            return

def selectKey():
    set_active_state("displaySelectKey")
    while True:
        key = digit()
        while key is None:
            buzzer.off()
        buzzer.on()
        sleep(0.05)
        buzzer.off()
        if key > 0 and key < 10:
            scanID()
            return  # Exit after scanning ID
        elif key == 0:
            return  # Exit to the previous menu

def scanID():
    set_active_state("displayScanID")
    uid = idScanner()
    buzzer.on()
    sleep(0.05)
    buzzer.off()
    if uid == "73de2a29":
        set_active_state("displayConfirm")
        sleep(1)
    else: 
        set_active_state("displayReject")
        sleep(1)
    return
    

def idScanner():
    cardData = reader.read_id()
    cardDataInHex = f"{cardData:x}"
    minusMfgID = cardDataInHex[:-2]
    return minusMfgID

# Start the threads
t1 = Thread(target=lcdScreenController)
t2 = Thread(target=main)

t1.start()
t2.start()