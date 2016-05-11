from pytrack import ImageProcessor
import sys
	
improc = ImageProcessor(
	frontal_classifier='cascade/haarcascade_frontalface_alt2.xml', 
	profile_classifier='cascade/haarcascade_profileface.xml',
	initial_x=sys.argv[1],
	initial_y=sys.argv[2],
	max_x=sys.argv[3],
	max_y=sys.argv[4]
)


improc.findObjects()
