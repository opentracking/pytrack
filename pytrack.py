import cv2
import sys
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

class ImageProcessor:
	def __init__(self, haarCascade):
		self.haarCascade = haarCascade
	
	def findObjects(self):
		# Create the haar cascade
		faceCascade = cv2.CascadeClassifier(self.haarCascade)

		old_x = 0
		old_y = 0

		camera = PiCamera()
		camera.resolution = (320, 240)
		camera.framerate = 32
		rawCapture = PiRGBArray(camera, size=(320, 240))

		time.sleep(0.1)

		for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
			# Resize and flip frame for better performance
	
			frame = cv2.flip(frame.array, 1)
			#frame = cv2.resize(cv2.flip(frame.array, 1), (320, 240))

			greyscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
			faces = faceCascade.detectMultiScale(
				greyscale_frame,
				scaleFactor = 1.3, 
				minNeighbors = 5,
				minSize = (15, 15),
				flags = cv2.CASCADE_SCALE_IMAGE
			)

			# Draw a rectangle around the faces
			if len(faces) > 1:
				closest_face = 0
				min_x = 1000
				min_y = 1000
				for i, (x, y, w, h) in enumerate(faces):
					if (x - old_x < min_x) and (y - old_y < min_y):
						closest_face = i
				x = faces[i][0]
				y = faces[i][1]
				w = faces[i][2]
				h = faces[i][3]
					
				print "x-offset: {}, y-offset: {}".format(old_x - x, old_y - y)
				# print "x: {}, y: {}, w: {}, h: {}".format(x, y, w, h)
				old_x = x
				old_y = y
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
			else:
				for (x, y, w, h) in faces:
					print "x-offset: {}, y-offset: {}".format(old_x - x, old_y - y)
					# print "x: {}, y: {}, w: {}, h: {}".format(x, y, w, h)
					old_x = x
					old_y = y
					cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

			# Display the resulting frame
			cv2.imshow('Video', frame)

			rawCapture.truncate(0)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
