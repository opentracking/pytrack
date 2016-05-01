import RPi.GPIO as GPIO
import time
import os

class Motor(object):
	def __init__(self):
		"""
		TO ADD
		"""

		self.delay = 0.06
		self.current_x = 135
		self.current_y = 90

		self.x_pin = 0
		self.y_pin = 1

		# Manually set the position to start
		self.pwm(self.x_pin, self.current_x, self.delay)
		self.pwm(self.y_pin, self.current_y, self.delay)

	def update_x(self, dx):
		"""
		dx : horizontal pixels from image center

		Update the servo horizontal position
		"""

		movement_x = self.current_x + dx
		
		self.pwm(self.x_pin, movement_x, self.delay)
		
		self.current_x = movement_x

	def update_y(self, dy):
		"""
		dy : vertical pixels from image center

		Update the servo vertical position
		"""

		movement_y = self.current_y + dy

		self.pwm(self.y_pin, movement_y, self.delay)

		self.current_y = movement_y

	def pwm(self,pin,offset,delay):
		"""
		pin    : GPIO pin of servo
		offset : Amount servo should move
		delay  : Amount of time to wait for the servo to move

		"""
		print("servo[" + str(pin) + "][" + str(offset) + "]")
		cmd = "echo " + str(pin) + "=" + str(offset) + " > /dev/servoblaster"
		os.system(cmd)
		time.sleep(delay)
	
