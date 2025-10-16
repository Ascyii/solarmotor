"""Helpers for building moving mirrors."""

class Motor:
    """Model a type of servo motor."""

    # Default vaules for every motor
    MAX_PULSE = 2500
    MIN_PULSE = 500
    COVERAGE = 180 # Total degree of freedom in degrees
    AREA = MAX_PULSE - MIN_PULSE
    OFFSET = 2 # In degrees a constant to be added
    SCALE = 1 # Scaling

    # Used for ids
    count = 0

    def __init__(self, pi, pin, angle=0):
        self.id = Motor.count; Motor.count += 1
        self.pi = pi # Local pi instance

        self.pin = pin
        self.angle = angle
        self.offset = Motor.OFFSET # Fine grained controls over every motor
        self.scale = Motor.SCALE

        # Initialization
        self.set()

    def angle_to_pulse(self, angle):
        return min(max(Motor.MIN_PULSE, (Motor.MIN_PULSE + Motor.AREA * angle/Motor.COVERAGE + self.offset) * self.scale), Motor.MAX_PULSE)

    # Update the motor position on hardware
    def set(self):
        self.pi.set_servo_pulsewidth(self.pin, self.angle_to_pulse(self.angle))

    def set_angle(self, angle):
        self.angle = angle
        self.set()

    def __str__(self):
        return f"Motor {self.id} is set at {self.angle} degrees."

    def __del__(self):
        self.pi.set_servo_pulsewidth(self.pin, 0)

    def inc(self, inc):
        self.angle += inc
        self.angle = min(max(self.angle, 0), Motor.COVERAGE) # Clip
        self.set()
