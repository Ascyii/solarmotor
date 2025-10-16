import pigpio
import RPi.GPIO as GPIO
import time
import os

from motor import Motor # Models the motor

# Constants
SERVO1_PIN = 18
SERVO2_PIN = 19

BUTTON1_FWD = 5
BUTTON1_BWD = 6
BUTTON2_FWD = 17
BUTTON2_BWD = 27
SHUTDOWN_BTN = 26

STEP = 2
LOOP_DELAY = 0.3 # In seconds

# Local pi
pi = pigpio.pi()
if not pi:
    os.exit()

# Setup the controls
GPIO.setmode(GPIO.BCM)
for btn in [BUTTON1_FWD, BUTTON1_BWD, BUTTON2_FWD, BUTTON2_BWD, SHUTDOWN_BTN]:
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Setup motors
m1 = Motor(pi, SERVO1_PIN)
m2 = Motor(pi, SERVO2_PIN)

# Main
try:
    while True:
        # Inputs shutdown
        if GPIO.input(SHUTDOWN_BTN) == GPIO.HIGH:
            os.system("sudo shutdown now")

        # Motors
        if GPIO.input(BUTTON1_FWD):
            m1.inc(STEP)
        elif GPIO.input(BUTTON1_BWD):
            m1.inc(-STEP)
        if GPIO.input(BUTTON2_FWD):
            m2.inc(STEP)
        elif GPIO.input(BUTTON2_BWD):
            m2.inc(-STEP)

        time.sleep(LOOP_DELAY)

except KeyboardInterrupt:
    pass

finally:
    del m1
    del m2
    pi.stop()
    GPIO.cleanup()
