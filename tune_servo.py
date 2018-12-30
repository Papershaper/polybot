from __future__ import division
import time
import sys
import Adafruit_PCA9685

if sys.argv < 4:
    print('arguments should be channel, min, max')

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()
servo_min = int(sys.argv[2])  # Min pulse length out of 4096
servo_max = int(sys.argv[3])  # Max pulse length out of 4096
# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

channel = int(sys.argv[1])
print('Moving servo on channel between min-max, press Ctrl-C to quit...')
while True:
    pwm.set_pwm(channel, 0, servo_min)
    time.sleep(1)
    pwm.set_pwm(channel, 0, servo_max)
    time.sleep(1)
