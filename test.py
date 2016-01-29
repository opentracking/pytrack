from pytrack import ImageProcessor
import sys

improc = ImageProcessor(sys.argv[1])
improc.findObjects()