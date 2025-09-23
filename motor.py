import pigpio
import RPi.GPIO as GPIO
import time
import os

# Constants
SERVO1_PIN = 18
SERVO2_PIN = 19

BUTTON1_FWD = 5
BUTTON1_BWD = 6
BUTTON2_FWD = 17
BUTTON2_BWD = 27
SHUTDOWN_BTN = 26

MIN_PULSE = 1000 # In ms
MAX_PULSE = 2000
INIT_PULSE = 1500
STEP = 10
LOOP_DELAY = 0.01 # In seconds

# Setup
GPIO.setmode(GPIO.BCM)
for btn in [BUTTON1_FWD, BUTTON1_BWD, BUTTON2_FWD, BUTTON2_BWD, SHUTDOWN_BTN]:
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pi = pigpio.pi()
if not pi.connected:
    print("Cannot connect to pigpio daemon!")
    exit()

pulse1 = INIT_PULSE
pulse2 = INIT_PULSE
pi.set_servo_pulsewidth(SERVO1_PIN, pulse1)
pi.set_servo_pulsewidth(SERVO2_PIN, pulse2)

# Helpers
def move_servo(current, target, step=STEP):
    if current < target:
        current = min(current + step, target)
    elif current > target:
        current = max(current - step, target)
    return current

# Main
try:
    while True:
        # Shutdown
        if GPIO.input(SHUTDOWN_BTN) == GPIO.HIGH:
            os.system("sudo shutdown now")

        # Motor 1
        target1 = pulse1
        if GPIO.input(BUTTON1_FWD):
            target1 = min(MAX_PULSE, pulse1 + STEP)
        elif GPIO.input(BUTTON1_BWD):
            target1 = max(MIN_PULSE, pulse1 - STEP)
        pulse1 = move_servo(pulse1, target1)
        pi.set_servo_pulsewidth(SERVO1_PIN, pulse1)

        # Motor 2
        target2 = pulse2
        if GPIO.input(BUTTON2_FWD):
            target2 = min(MAX_PULSE, pulse2 + STEP)
        elif GPIO.input(BUTTON2_BWD):
            target2 = max(MIN_PULSE, pulse2 - STEP)
        pulse2 = move_servo(pulse2, target2)
        pi.set_servo_pulsewidth(SERVO2_PIN, pulse2)

        time.sleep(LOOP_DELAY)

except KeyboardInterrupt:
    pass

finally:
    pi.set_servo_pulsewidth(SERVO1_PIN, 0)
    pi.set_servo_pulsewidth(SERVO2_PIN, 0)
    pi.stop()
    GPIO.cleanup()
