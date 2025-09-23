import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

# Servo pins
SERVO1_PIN = 19
SERVO2_PIN = 18

# Buttons
BUTTON1_FWD = 5   # Motor1 forward
BUTTON1_BWD = 6   # Motor1 backward
BUTTON2_FWD = 17  # Motor2 forward
BUTTON2_BWD = 27  # Motor2 backward
SHUTDOWN_BTN = 26 # Shutdown button

# Setup buttons (pulled down, pressed = HIGH)
for button in [BUTTON1_FWD, BUTTON1_BWD, BUTTON2_FWD, BUTTON2_BWD, SHUTDOWN_BTN]:
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Setup servo pins
GPIO.setup(SERVO1_PIN, GPIO.OUT)
GPIO.setup(SERVO2_PIN, GPIO.OUT)

servo1 = GPIO.PWM(SERVO1_PIN, 50)  # 50Hz
servo2 = GPIO.PWM(SERVO2_PIN, 50)
servo1.start(0)
servo2.start(0)

# ----------------------------
# Helpers
# ----------------------------
def pulse_to_duty(pulse_us):
    return (pulse_us / 20000.0) * 100.0  # 20ms period → duty %

# Pulse limits
STOP_PULSE = 1500
MIN_PULSE  = 1000
MAX_PULSE  = 1500

# Initialize at 1200 µs
INIT_PULSE = 1200
servo1.ChangeDutyCycle(pulse_to_duty(INIT_PULSE))
servo2.ChangeDutyCycle(pulse_to_duty(INIT_PULSE))

# ----------------------------
# Main loop
# ----------------------------
try:
    while True:
        if GPIO.input(SHUTDOWN_BTN) == GPIO.HIGH:
            os.system("sudo shutdown now")

        # Motor 1
        if GPIO.input(BUTTON1_FWD) == GPIO.HIGH:
            servo1.ChangeDutyCycle(pulse_to_duty(MAX_PULSE))
        elif GPIO.input(BUTTON1_BWD) == GPIO.HIGH:
            servo1.ChangeDutyCycle(pulse_to_duty(MIN_PULSE))
        else:
            servo1.ChangeDutyCycle(pulse_to_duty(STOP_PULSE))

        # Motor 2
        if GPIO.input(BUTTON2_FWD) == GPIO.HIGH:
            servo2.ChangeDutyCycle(pulse_to_duty(MAX_PULSE))
        elif GPIO.input(BUTTON2_BWD) == GPIO.HIGH:
            servo2.ChangeDutyCycle(pulse_to_duty(MIN_PULSE))
        else:
            servo2.ChangeDutyCycle(pulse_to_duty(STOP_PULSE))

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    servo1.stop()
    servo2.stop()
    GPIO.cleanup()
