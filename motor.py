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

# Setup buttons
buttons = [BUTTON1_FWD, BUTTON1_BWD, BUTTON2_FWD, BUTTON2_BWD, SHUTDOWN_BTN]
for button in buttons:
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Setup servo pins
GPIO.setup(SERVO1_PIN, GPIO.OUT)
GPIO.setup(SERVO2_PIN, GPIO.OUT)

# PWM setup for servo motors (50Hz typical for servos)
servo1 = GPIO.PWM(SERVO1_PIN, 50)
servo2 = GPIO.PWM(SERVO2_PIN, 50)
servo1.start(0)
servo2.start(0)

# ----------------------------
# Speed variable (0-100%)
# ----------------------------
speed = 50  # Default speed percentage

# Function to convert speed to duty cycle for servo (1-2 ms pulse)
def speed_to_duty(speed_percent):
    # 1 ms = 5% duty, 2 ms = 10% duty at 50Hz
    # Map speed 0-100% to 5-10% duty cycle
    duty = 5 + (speed_percent / 100) * 5
    return duty

# ----------------------------
# Main loop
# ----------------------------
try:
    while True:
        if GPIO.input(SHUTDOWN_BTN) == GPIO.HIGH:
            print("Shutting down...")
            os.system("sudo shutdown now")
        
        # Motor 1
        if GPIO.input(BUTTON1_FWD) == GPIO.HIGH:
            servo1.ChangeDutyCycle(speed_to_duty(speed))
            print("Pressed.")
        elif GPIO.input(BUTTON1_BWD) == GPIO.HIGH:
            servo1.ChangeDutyCycle(speed_to_duty(100 - speed)) # backward
            print("Pressed.")
        else:
            servo1.ChangeDutyCycle(0)  # stop
        
        # Motor 2
        if GPIO.input(BUTTON2_FWD) == GPIO.HIGH:
            servo2.ChangeDutyCycle(speed_to_duty(speed))
            print("Pressed.")


        elif GPIO.input(BUTTON2_BWD) == GPIO.HIGH:
            servo2.ChangeDutyCycle(speed_to_duty(100 - speed)) # backward
            print("Pressed.")


        else:
            servo2.ChangeDutyCycle(0)  # stop

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    servo1.stop()
    servo2.stop()
    GPIO.cleanup()

