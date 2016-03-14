from pytrack import *

def frameOffset():
	imgproc = ImageProcessor()
	leftFace  = imgproc.analyzeFrame('unitTestPhotos/left.jpg')[0]
	rightFace = imgproc.analyzeFrame('unitTestPhotos/right.jpg')[0]

	imageWidth  = 2592
	imageHeight = 1994

	if not leftFace.any():
		print "Could not find a left face"
		return
	if not rightFace.any():
		print "Could not find a right face"
		return

	xOffset = abs(leftFace[0][0] - rightFace[0][0])
	yOffset = abs(leftFace[0][1] - rightFace[0][1])

	if xOffset > (imageWidth/2)  and xOffset < (imageWidth/2+(imageWidth*.1)):
		return True
	else:
		print "xOffset not in correct range"
		return False

def multipleFaces():
	imgproc = ImageProcessor()
	faces = imgproc.analyzeFrame('unitTestPhotos/multiple.jpg')[0]

	if not faces.any():
		print "Could not find a face"
		return

	imageWidth  = 2592
	imageHeight = 1994

	oldX = imageWidth/2
	oldY = imageHeight/2

	if len(faces) > 1:
     	closestFace = 0
        minX = 1000
        minY = 1000
        for i, (x, y, w, h) in enumerate(faces):
            if (x - oldX < minX) and (y - oldY < minY):
                    closestFace = i
        x = faces[closestFace][0]
        y = faces[closestFace][1]
        w = faces[closestFace][2]
     	h = faces[closestFace][3]

    elif len(faces) == 1:
        x = faces[0][0]
        y = faces[0][1]
        w = faces[0][2]
        h = faces[0][3]
    else:
        x = -1
        y = -1
        w = -1
		h = -1

	print x
	if x > (.75 * 1296) and x < (1.25 * 1296):
		return True
	else:
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
