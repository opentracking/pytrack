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
	new_pos = self.current + deg_x
	if new_pos < 2:
		new_pos = 2
	if new_pos > 11.5:
		new_pos = 11.5
	self.pwm.start(new_pos)
	self.current = new_pos

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

	
