#!/usr/bin/env python
import RPi.GPIO as gpio
import time
import sys


def isDoorClosed():

    gpio.setmode(gpio.BCM)
    trig = 27 # 7th
    echo = 17 # 6th

    gpio.setup(trig, gpio.OUT)
    gpio.setup(echo, gpio.IN)


    time.sleep(0.5)
    try :
        while True :
            gpio.output(trig, False)
            time.sleep(0.1)
            gpio.output(trig, True)
            time.sleep(0.00001)
            gpio.output(trig, False)
            while gpio.input(echo) == 0 :
                pulse_start = time.time()
            while gpio.input(echo) == 1 :
                pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17000
            if pulse_duration >=0.01746:
                print('time out')
                continue
            elif distance < 5 or distance == 0:
                print('ok')
                continue
            elif distance > 5 or distance==0:
                print('gago sara mo pinto haha')
                continue
            distance = round(distance, 3)
            print ('Distance : %f cm'%distance)

    except (KeyboardInterrupt, SystemExit):
        gpio.cleanup()
        sys.exit(0)
    except:
        gpio.cleanup()

