import RPi.GPIO as GPIO
import time
import os

class Motor(object):
	def __init__(self, delay=0.06, current_x=135, current_y=90, x_pin=0, y_pin=1, max_x=10, max_y=5):
		"""
		TO ADD
		"""

		self.delay = delay
		self.current_x = current_x
		self.current_y = current_y

		self.x_pin = x_pin
		self.y_pin = y_pin

		self.max_x = max_x
		self.max_y = max_y


		# Manually set the position to start
		self.pwm(self.x_pin, self.current_x, self.delay)
		self.pwm(self.y_pin, self.current_y, self.delay)

	def update_x(self, dx):
		"""
		dx : horizontal pixels from image center

		Update the servo horizontal position
		"""

		if abs(dx) > self.max_x:
			dx = (-1 if dx < 0 else 1) * self.max_x

		movement_x = self.current_x + dx
		
		self.pwm(self.x_pin, movement_x, self.delay)
		
		self.current_x = movement_x

	def update_y(self, dy):
		"""
		dy : vertical pixels from image center

		Update the servo vertical position
		"""

		if abs(dy) > self.max_y:
			dy = (-1 if dy < 0 else 1) * self.max_y

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
	
