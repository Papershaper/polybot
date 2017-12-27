#!/usr/bin/env python
#
#  poly_drive.py
#  Copyright 2017  Doug Taylor <pi@polybase>

import RPi.GPIO as gpio
import time

step_duration = 0.5 #seconds
motor_pinEnable = 12  #enable Motor
motor_pinA = 16  #motor in-1
motor_pinB = 18  #motor in-2
steer_pinEnable = 7  #enable Steering
steer_pinA = 13  #steer in-3
steer_pinB = 15  #steer in-4

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
			
def main():
	init_gpio()
	try:
		while(True):
			message = raw_input("Enter Command: ")
			drive_command(message)
			#drive_command(command)
	finally:
		print("exiting clean")
		gpio.cleanup()
			
	return 0

if __name__ == '__main__':
	main()

