import RPi.GPIO as GPIO
import time

# ----------------------------
# Setup
# ----------------------------
GPIO.setmode(GPIO.BCM)      # Use BCM numbering
PIN = 26                    # The pin you want to monitor (BCM26)

# Setup pin as input with pull-up
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print(f"Monitoring GPIO{PIN}. Press Ctrl+C to exit.")

try:
    while True:
        if GPIO.input(PIN):   # Pin is HIGH (1)
            print(f"GPIO{PIN} is HIGH")
        else:                 # Pin is LOW (0)
            print(f"GPIO{PIN} is LOW")
        time.sleep(0.1)       # Check every 100 ms

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()

