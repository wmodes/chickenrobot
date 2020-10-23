from time import sleep
import RPi.GPIO as GPIO

DIR = 20    # Direction GPIO pin
STEP = 21   # Step GPIO pin
CW = 1      # Clockwise rotation
CCW = 0     # Anti-clockwise rotation
SPR = 200    # Steps per revolution (360/1.8) from stepper datasheet

step_count = SPR
delay = 0.005   # 1 second / SPR

GPIO.setmode(GPIO.BCM)

for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

sleep(0.5)
GPIO.output(DIR, CCW)

for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)
