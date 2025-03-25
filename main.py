from lcd_controller import lcdScreenController, set_active_state
from lock_controller import changeLockState
from threading import Thread
from matrix_driver import keypad
from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from gpiozero import Buzzer
import requests
import json
import datetime

kp = keypad()
buzzer = Buzzer(26)
reader = SimpleMFRC522()
uid_test = "73de2a29"
BASE_API_URL = "https://keycabinet.cspc.edu.ph/api/"

key = 0
keyID = 0
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
        if key == 1:
            key = None
            displayMain()
        else:
            print(key)
            print('Invalid key')
            continue  # Exit the loop if 0 is pressed

def displayMain():
    set_active_state("displayMainMenu")
    global key
    while True:
        key = digit()
        buzzer.on()
        sleep(0.05)
        buzzer.off()
        print(key)
        if key == "*":
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
    global keyID
    while True:
        key = digit()
        keyID = key
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
    uid = str(idScanner())
    buzzer.on()
    sleep(0.05)
    buzzer.off()
    status = getIDholder(uid)
    if status[0] == 200:
        set_active_state("displayConfirm")
        headers = {'content-type': 'application/json', 'accepts': 'application/json'}
        res = requests.post('https://keycabinet.cspc.edu.ph/logs/store', json={
        "faculty_id" : status[1],
        "key_id": keyID,
        "details": "Borrowed laboratory key",
        "date_time_borrowed": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }, headers = headers)
        changeLockState('unlock')
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

def getIDholder(uid):
    req = requests.get(BASE_API_URL + "faculty")
    result = req.json()
    
    for _faculty in range(len(result)):
        if(str(uid) == result[_faculty]['rfid_uid']):
            if (result[_faculty]['status'] == "Disabled"):
                return [403, result[_faculty]["faculty_id"]]
            else:
                return [200, result[_faculty]["faculty_id"]]
        else:
            continue
    return [404, None]
    
    
# Start the threads
t1 = Thread(target=lcdScreenController)
t2 = Thread(target=main)
t1.start()
t2.start()