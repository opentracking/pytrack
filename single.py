from pytrack import ImageProcessor
import sys

improc = ImageProcessor(
	frontal_classifier=sys.argv[1], 
	profile_classifier=None,
	initial_x = sys.argv[2],
	initial_y = sys.argv[3],
	max_x = sys.argv[4],
	max_y = sys.argv[5]
)

improc.findObjects()
