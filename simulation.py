import pigpio
import RPi.GPIO as GPIO
import time

# Solar module for simulation of world
import solar # Modeling of the world
from motor import Motor # Small helper functions and constants

# Constants
SERVO1_PIN = 18
SERVO2_PIN = 19

INIT_PULSE = 0
STEP = 10
LOOP_DELAY = 0.01 # In seconds

pi = pigpio.pi()
if not pi.connected:
    print("Cannot connect to pigpio daemon!")
    exit()

angle1 = init_motor(SERVO1_PIN)
angle2 = init_motor(SERVO2_PIN)

# Testing embedding the mirrors in the world
world = solar.World(tilt_deg=15)  # The world is tilted 15 degrees around y-axis

HEIGHT = 30

source = solar.Source(world, pos=(0, 0, 30))
target = solar.Target(world, pos=(20, 0, 30))

# Create mirrors in a 9x9 grid
for x in range(3):
    for y in range(3):
        mirror = solar.Mirror(world, cluster_x=x, cluster_y=y)
        world.add_mirror(mirror)

world.update_mirrors_from_source_target(source, target)

for i, mirror in enumerate(world.mirrors):
    pitch, yaw = mirror.get_angles()
    print(f"Mirror {i} ({mirror.cluster_x}, {mirror.cluster_y}) angles -> pitch: {pitch:.2f}°, yaw: {yaw:.2f}°")

def sm1(a): # Set motor 1
    pi.set_servo_pulsewidth(SERVO1_PIN, angle_to_pulse(a))
    time.sleep(2)


angle = 150
time.sleep(10)

sm1(150)
sm1(90)
sm1(0)
sm1(180)
sm1(30)
sm1(120)
sm1(60)
sm1(30)
sm1(180)
sm1(120)
sm1(30)
sm1(150)
sm1(3)



# Main
try:
    while True:
        # Shutdown
        if GPIO.input(SHUTDOWN_BTN) == GPIO.HIGH:
            os.system("sudo shutdown now")

        pulse1 = angle_to_pulse(angle)
        time.sleep(3)
        angle += 10

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
