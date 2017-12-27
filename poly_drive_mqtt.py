#!/usr/bin/env python
#
#  poly_drive_mqtt.py
#  poly drive code with mqtt subscription. 
#  Recieve drive commands via mqtt.  Topic "polybot/command"
#  Copyright 2017  Doug Taylor <pi@polybase>

import RPi.GPIO as gpio
import time
import paho.mqtt.client as mqtt

broker="192.168.178.88" #config, change to matach

step_duration = 0.5 #seconds
motor_pinEnable = 12  #enable Motor
motor_pinA = 16  #motor in-1
motor_pinB = 18  #motor in-2
steer_pinEnable = 7  #enable Steering
steer_pinA = 13  #steer in-3
steer_pinB = 15  #steer in-4

#GPIO control section -----------------
def init_gpio():
	gpio.setmode(gpio.BOARD)
	gpio.setup(motor_pinEnable, gpio.OUT)
	gpio.setup(motor_pinA, gpio.OUT)
	gpio.setup(motor_pinB, gpio.OUT)
	gpio.setup(steer_pinEnable, gpio.OUT)
	gpio.setup(steer_pinA, gpio.OUT)
	gpio.setup(steer_pinB, gpio.OUT)
	
def set_forward():
	print("forward")
	gpio.output(motor_pinA, False)
	gpio.output(motor_pinB, True)
	gpio.output(motor_pinEnable, True)


def set_reverse():
	print("Reverse")
	gpio.output(motor_pinA, True)
	gpio.output(motor_pinB, False)
	gpio.output(motor_pinEnable, True)
	
def set_left():
	print("Left")
	gpio.output(steer_pinEnable, True)
	gpio.output(steer_pinA, True)
	gpio.output(steer_pinB, False)
	
def set_right():
	print("Right")
	gpio.output(steer_pinEnable, True)
	gpio.output(steer_pinA, False)
	gpio.output(steer_pinB, True)
	
def disable_pins():
	gpio.output(motor_pinEnable, False)
	gpio.output(steer_pinEnable, False)
	
def drive_command(cmd):
	#CMD should be motor,steer,duration
	#set motor direction
	if(cmd[0] == 'F'):
		set_forward()
	else:
		set_reverse()
	#set steer direction
	if(cmd[1] == 'L'):
		set_left()
	elif (cmd[1] == 'R'):
		set_right()
	# ELSE straight - no turn
	#drive duration
	print("duration: "+cmd[2])
	time.sleep((float(cmd[2])*step_duration))
	
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
		client.subscribe("polybot/command", 0)
		client.loop_forever()
		
	finally:
		print("exiting clean")
		gpio.cleanup()
			
	return 0

if __name__ == '__main__':
	main()

