from pytrack import ImageProcessor
import sys

if len(sys.argv) > 1:
	improc = ImageProcessor(sys.argv[1])
else:
	improc = ImageProcessor()

improc.findObjects()
