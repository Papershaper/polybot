#!/usr/bin/env python
#
#  robot_arcade.py
#  code with mqtt subscription. 
#  Recieve drive commands via mqtt.  Topic "LR/command"
#  Copyright 2018  Doug Taylor  totally not evil robot army

import RPi.GPIO as gpio
import time
import paho.mqtt.client as mqtt

broker="192.168.178.88" #TODO config, change to matach

step_duration = 0.5 #seconds
#motor_pinEnable = 12  #enable Motor
m1_pinA = 16  #motor in-1
m1_pinB = 18  #motor in-2
#steer_pinEnable = 7  #enable Steering
m2_pinA = 13  #motor in-3
m2_pinB = 15  #motor in-4

#GPIO control section -----------------
def init_gpio():
	gpio.setmode(gpio.BOARD)
	#gpio.setup(motor_pinEnable, gpio.OUT)
	gpio.setup(m1_pinA, gpio.OUT)
	gpio.setup(m1_pinB, gpio.OUT)
	#gpio.setup(steer_pinEnable, gpio.OUT)
	gpio.setup(m2_pinA, gpio.OUT)
	gpio.setup(m2_pinB, gpio.OUT)
	
def set_forward():
	print("forward")
	gpio.output(m1_pinA, False)
	gpio.output(m1_pinB, True)
	#gpio.output(motor_pinEnable, True)

def set_reverse():
	print("Reverse")
	gpio.output(m1_pinA, True)
	gpio.output(m1_pinB, False)
	#gpio.output(motor_pinEnable, True)
	
def set_left():
	print("Left")
	#gpio.output(steer_pinEnable, True)
	gpio.output(m2_pinA, True)
	gpio.output(m2_pinB, False)
	
def set_right():
	print("Right")
	#gpio.output(steer_pinEnable, True)
	gpio.output(m2_pinA, False)
	gpio.output(m2_pinB, True)
	
def disable_pins():
	#gpio.output(motor_pinEnable, False)
	#gpio.output(steer_pinEnable, False)
	gpio.output(m1_pinA, False)
	gpio.output(m1_pinB, False)
	gpio.output(m2_pinA, False)
	gpio.output(m2_pinB, False)
	
def drive_command(cmd):
	#CMD should be motor,steer,duration
	#set motor direction
	if(cmd[0] == 'F'):
		set_forward()
	if(cmd[0] == 'B'):
		set_reverse()
	#set steer direction
	if(cmd[0] == 'L'):
		set_left()
	if (cmd[0] == 'R'):
		set_right()
	# ELSE straight - no turn
	#drive duration --- override  just 1second
	print("duration: "+cmd[2])
	#time.sleep((float(cmd[2])*step_duration))
	time.sleep(1)

	#shut off motors
	disable_pins()

# MQTT section ------------------------------
def on_connect(client, obj, flags, rc):
	print("connect rc:"+str(rc))

def on_subscribe(client, obj, mid, granted_qos):
	print("subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, message):
	cmd = str(message.payload.decode("utf-8"))
	print("recieved messsage=> "+cmd)
	drive_command(cmd)


# Main --------------------------------------
def main():
	init_gpio()
	client = mqtt.Client()
	client.on_message = on_message
	client.on_connect = on_connect
	client.on_subscribe = on_subscribe
	
	try:
		client.connect(broker, 1883, 60)
		client.subscribe("LR/command", 0)
		client.loop_forever()
		
	finally:
		print("exiting clean")
		gpio.cleanup()
			
	return 0

if __name__ == '__main__':
	main()

