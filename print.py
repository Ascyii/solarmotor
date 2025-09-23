import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)
PIN = 26

# Setup pin as input with pull-up
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print(f"Monitoring GPIO{PIN}. Press Ctrl+C to exit.")

try:
    while True:
        if GPIO.input(PIN):
            print(f"GPIO{PIN} is HIGH")
        else:
            print(f"GPIO{PIN} is LOW")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
