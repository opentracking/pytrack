from pytrack import *

def frameOffset():
	imgproc = ImageProcessor()
	leftFace  = imgproc.analyzeFrame('unitTestPhotos/left.jpg')[0]
	rightFace = imgproc.analyzeFrame('unitTestPhotos/right.jpg')[0]

	xOffset = abs(leftFace[0][0] - rightFace[0][0])
	yOffset = abs(leftFace[0][1] - rightFace[0][1])

	print xOffset
	print yOffset

	#print xOffset
	#print yOffset

	return False

def multipleFaces():
	return False

# Run tests
if frameOffset():
	print "frameOffset test passed"
else:
	print "frameOffset test failed"

if multipleFaces():
	print "multipleFaces test passed"
else:
	print "multipleFaces test failed"
