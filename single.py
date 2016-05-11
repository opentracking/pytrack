from pytrack import ImageProcessor
import sys

improc = ImageProcessor(frontal_classifier=sys.argv[1], profile_classifier=None,SM=sys.argv[2],MM=sys.argv[3],LM=sys.argv[4])

improc.findObjects()
