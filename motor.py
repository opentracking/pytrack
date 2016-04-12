import RPi.GPIO as GPIO
import time
import os

class Motor(object):
    def __init__(self, pixels_x, pixels_y, fov_x, fov_y, gpioX=18,gpioY=23):
        """
        pixels_x : number of horizontal pixels of image capture
        pixels_y : number of vertical pixels of image capture
        fov_x : degrees of horizontal camera perspective
        fov_y : degrees of vertical camera perspective
        """

		self.min = 50
		self.max = 220
		self.delay = 0.06
		self.current_x = 135
		self.current_y = 135

		self.x_pin = 0
		self.y_pin = 1

	    self.pixels_x = float(pixels_x)
	    self.pixels_y = float(pixels_y)
	    self.fov_x = float(fov_x)
	    self.fov_y = float(fov_y)

		# Manually set the position to start
		self.pwm(0,self.current_x,self.delay)
		self.pwm(1,self.current_y,self.delay)

    def update_x(self, dx):
        """
        dx : horizontal pixels from image center

        Update the servo horizontal position
        """

		movement_x = self.current_x + offset_x

		self.pwm(self.x_pin,movement_x,self.delay)

		self.current = movement_x

	def update_y(self, dy):
        """
        dy : vertical pixels from image center

        Update the servo vertical position
        """

		movement_y = self.current_x + offset_y

		self.pwm(self.y_pin,movement_y,self.delay)

		self.current = movement_y

	def pwm(self,pin,offset,delay):
		"""
		pin    : GPIO pin of servo
		offset : Amount servo should move
		delay  : Amount of time to wait for the servo to move

		"""
		print "servo[" + str(pin) + "][" + str(offset) + "]"
        cmd = "echo " + str(pin) + "=" + str(offset) + " > /dev/servoblaster"
        os.system(cmd)
        time.sleep(delay)

	
