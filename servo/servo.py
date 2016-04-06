import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
pwm = GPIO.PWM(18,50)
pwm.start(2)

# This seems to be a good value for a 10% change in duty cycle
delay = 0.06
while True:
	for i in range(2,11):
		time.sleep(delay)
		pwm.start(i)
	for i in reversed(range(2,11)):
		time.sleep(delay)
		pwm.start(i)
		