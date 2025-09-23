import pigpio
import RPi.GPIO as GPIO
import time
import os

# Solar module for simulation of world
import solar

# Constants
SERVO1_PIN = 18
SERVO2_PIN = 19

BUTTON1_FWD = 5
BUTTON1_BWD = 6
BUTTON2_FWD = 17
BUTTON2_BWD = 27
SHUTDOWN_BTN = 26

MIN_PULSE = 500 # In ms
MAX_PULSE = 2500
INIT_PULSE = 1000
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

# Testing embedding the mirrors in the world
world = solar.World(tilt_deg=15)  # The world is tilted 15 degrees around y-axis

source = solar.Source(world, pos=(100, 100, 100))
target = solar.Target(world, pos=(50, 50, 0))

# Create mirrors in a 9x9 grid
for x in range(3):
    for y in range(3):
        mirror = solar.Mirror(world, cluster_x=x, cluster_y=y)
        world.add_mirror(mirror)

world.update_mirrors_from_source_target(source, target)

for i, mirror in enumerate(world.mirrors):
    pitch, yaw = mirror.get_angles()
    print(f"Mirror {i} ({mirror.cluster_x}, {mirror.cluster_y}) angles -> pitch: {pitch:.2f}°, yaw: {yaw:.2f}°")

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
