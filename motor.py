import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

# Servo pins
SERVO1_PIN = 19
SERVO2_PIN = 18

# Buttons
BUTTON1_FWD = 5   # Motor1 increase speed
BUTTON1_BWD = 6   # Motor1 decrease speed
BUTTON2_FWD = 17  # Motor2 increase speed
BUTTON2_BWD = 27  # Motor2 decrease speed
SHUTDOWN_BTN = 26 # Shutdown button

# Setup buttons
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
MIN_PULSE = 1000
MAX_PULSE = 1500
INIT_PULSE = 1200
STEP = 10  # how much to change per press (µs)

# Speed variables
pulse1 = INIT_PULSE
pulse2 = INIT_PULSE

# Initialize servos
servo1.ChangeDutyCycle(pulse_to_duty(pulse1))
servo2.ChangeDutyCycle(pulse_to_duty(pulse2))

# ----------------------------
# Main loop
# ----------------------------
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

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    servo1.stop()
    servo2.stop()
    GPIO.cleanup()
