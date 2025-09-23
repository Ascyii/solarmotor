import RPi.GPIO as GPIO
import time
import os

# Use the fat numberings
GPIO.setmode(GPIO.BCM)

# Constants
SERVO1_PIN = 18
SERVO2_PIN = 19
BUTTON1_FWD = 5   # Motor1
BUTTON1_BWD = 6
BUTTON2_FWD = 17  # Motor2
BUTTON2_BWD = 27
SHUTDOWN_BTN = 26 # Shutdown rpi

# Setup pins
for button in [BUTTON1_FWD, BUTTON1_BWD, BUTTON2_FWD, BUTTON2_BWD, SHUTDOWN_BTN]:
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SERVO1_PIN, GPIO.OUT)
GPIO.setup(SERVO2_PIN, GPIO.OUT)

servo1 = GPIO.PWM(SERVO1_PIN, 50)
servo2 = GPIO.PWM(SERVO2_PIN, 50)
servo1.start(0)
servo2.start(0)

# Adjust this for maximum range
def pulse_to_duty(pulse_us):
    return (pulse_us / 20000.0) * 100.0

# Pulse limits
MIN_PULSE = 1000
MAX_PULSE = 2000
INIT_PULSE = 1500
STEP = 10 # Adjust smoothness
SLEEP = 0.005

# Initialize servos
pulse1 = INIT_PULSE
pulse2 = INIT_PULSE
servo1.ChangeDutyCycle(pulse_to_duty(pulse1))
servo2.ChangeDutyCycle(pulse_to_duty(pulse2))

# Main loop
try:
    while True:
        if GPIO.input(SHUTDOWN_BTN) == GPIO.HIGH:
            os.system("sudo shutdown now")

        # Motor 1
        if GPIO.input(BUTTON1_FWD) == GPIO.HIGH:
            pulse1 = min(MAX_PULSE, pulse1 + STEP)
        elif GPIO.input(BUTTON1_BWD) == GPIO.HIGH:
            pulse1 = max(MIN_PULSE, pulse1 - STEP)
        servo1.ChangeDutyCycle(pulse_to_duty(pulse1))

        # Motor 2
        if GPIO.input(BUTTON2_FWD) == GPIO.HIGH:
            pulse2 = min(MAX_PULSE, pulse2 + STEP)
        elif GPIO.input(BUTTON2_BWD) == GPIO.HIGH:
            pulse2 = max(MIN_PULSE, pulse2 - STEP)
        servo2.ChangeDutyCycle(pulse_to_duty(pulse2))

        time.sleep(SLEEP)

except KeyboardInterrupt:
    pass

finally:
    servo1.stop()
    servo2.stop()
    GPIO.cleanup()
