import cv2
import sys
from picamera import PiCamera
from picamera.array import PiRGBArray
import time


# Get user supplied values
cascPath = sys.argv[1]

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

old_x = 0
old_y = 0

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# Resize and flip frame for better performance
	
	#small_frame = frame.array
	small_frame = cv2.resize(cv2.flip(frame.array, 1), (320, 240))

	gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor = 1.3, 
		minNeighbors = 5,
		minSize = (15, 15),
		flags = cv2.CASCADE_SCALE_IMAGE
	)

	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		print "x-offset: {}, y-offset: {}".format(old_x - x, old_y - y)
		# print "x: {}, y: {}, w: {}, h: {}".format(x, y, w, h)
		old_x = x
		old_y = y
		cv2.rectangle(small_frame, (x, y), (x+w, y+h), (0,255,0), 2)

	# Display the resulting frame
	cv2.imshow('Video', small_frame)

	rawCapture.truncate(0)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

