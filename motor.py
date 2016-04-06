import RPi.GPIO as GPIO

class Motor(object):
    def __init__(self, pixels_x, pixels_y, fov_x, fov_y, gpioX=18,gpioY=23):
        """
        pixels_x : number of horizontal pixels of image capture
        pixels_y : number of vertical pixels of image capture
        fov_x : degrees of horizontal camera perspective
        fov_y : degrees of vertical camera perspective
        """

	GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpioX,GPIO.OUT)
        self.pwm = GPIO.PWM(gpioX,50)
	self.current = 6.75
	self.dir = 1

        self.pixels_x = float(pixels_x)
        self.pixels_y = float(pixels_y)
        self.fov_x = float(fov_x)
        self.fov_y = float(fov_y)
        
        # user implements this function
        # self.move(deg_x, deg_y)
        #     """
        #     Rotate the horizontal and vertical motors to rotate orientation
        #     by deg_x and deg_y degrees respectively.
        #     """
    def move(self, deg_x,deg_y):
	print "deg_x: %s, deg_y: %s" % (deg_x,deg_y)
	# TO FIX
	# Need to change degrees to 2-11.5 
	#new_pos = self.current + 1
	#print "new_pos: %s" % new_pos
	#if new_pos < 2:
	#	new_pos = 2
	#if new_pos > 11.5:
	#	new_pos = 11.5
	#self.pwm.start(new_pos)
	#self.current = new_pos
	
	if self.dir:
		self.current += 1
	if self.current > 11.5:
		self.dir = 0
		self.current -= 1
	if not self.dir:
		self.current -= 1
	if self.current < 2:
		self.dir = 1
		self.current += 1
	self.pwm.start(self.current)

    def update(self, dx, dy):
        """
        dx : horizontal pixels from image center
        dy : vertical pixels from image center

        Update the camera position by calculating the number of degrees the
        camera needs to be moved.
        """

        deg_x = float(dx) * self.fov_x / self.pixels_x
        deg_y = float(dy) * self.fov_y / self.pixels_y

        #print "motor.move(%f, %f)" % (deg_x, deg_y)

        self.move(deg_x, deg_y)

	
