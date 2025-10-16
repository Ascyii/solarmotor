# Solarmotor

Mobilizing mirror cluster.

## Information

Use adafruit servokit to manage the servos through the external board.
Enable the I2C module for the rasberry pi.
Install the package and initialize with

```python
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
kit.servo[0].angle = 180
```
