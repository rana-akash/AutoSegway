import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)

gpio.setup(17,gpio.OUT)
gpio.setup(18,gpio.OUT)

while True:
    try:
        print('stopping drive')
        gpio.output(17,gpio.HIGH)
        gpio.output(18,gpio.HIGH)
        time.sleep(5)
        print('starting drive')
        gpio.output(17,gpio.LOW)
        gpio.output(18,gpio.LOW)
        time.sleep(5)
    except(KeyboardInterrupt):
        gpio.output(17,GPIO.LOW)
        gpio.output(18,GPIO.LOW)
        print('Interrupted')
    
    