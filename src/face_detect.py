import cv2
import sys

# Get user supplied values
cascPath = sys.argv[1]

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

old_x = 0
old_y = 0
while True:
	ret, frame = video_capture.read()	
	# Resize and flip frame for better performance
	small = cv2.resize(cv2.flip(frame, 1), (640, 360))

	gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

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
		cv2.rectangle(small, (x, y), (x+w, y+h), (0,255,0), 2)

	# Display the resulting frame
	cv2.imshow('Video', small)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()