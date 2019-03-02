# polybot
Primary project repo for polybot code.  Polybot is a robot concept where plugable parts work together to control the robot.  At this stage it is mostly a collection of python scripts that I use to share between the Raspberry Pis in my robot army.

Two types of two motor steering:
- basic GPIO commands for steering 2 motors in an RC car.  1 motor for Drive, 1 motor for Steering
- "crawler" code, wher GPIO command forward/backward on a left and right motor.

MQTT version subscribes to a MQTT broker and listens for commands

Suggest:
Use Eclipse Foundation Mosquitto Broker and Client

requires:  paho-mqtt python library
'sudo pip install paho-mqtt'

Servo code is using the adafruit PCA9685 libraries
