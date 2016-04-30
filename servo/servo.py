#!/usr/bin/env python
import time
import os
 
STEP = 10
DELAY = 0.06
 
min = 50
max = 220
# middle is approx = 140
def pwm(pin, angle):
	print "servo[" + str(pin) + "][" + str(angle) + "]"
	cmd = "echo " + str(pin) + "=" + str(angle) + " > /dev/servoblaster"
	os.system(cmd)
	time.sleep(DELAY)
 
while True:
	for j in range(min, max, STEP):
			pwm(0,j)
	for j in range(max, min, (STEP*-1)):
			pwm(0,j)
