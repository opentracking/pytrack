import sys
sys.path.append('/usr/local/lib/python2.7/site-packages/cv2.so')
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import RPi.GPIO as GPIO
from motor import Motor

# servoblaster control signals
SM = 4
MM = 6
LM = 8

class ImageProcessor:
	"""
	Uses a Haar cascade to detect objects and processes the image with OpenCV
	as well as sending control signals to servo motors.
	"""
		
	def __init__(self, frontal_face='cascade/haarcascade_frontalface_default.xml', profile_face='cascade/haarcascade_profileface.xml'):
		"""
		Initializes the Haar cascade with the given xml file path and creates a
		motor object.
		"""
		self.frontal_classifier = cv2.CascadeClassifier(frontal_face)
		self.profile_classifier = cv2.CascadeClassifier(profile_face)
		self.motor = Motor()
		
		self.camera = PiCamera()
		self.camera.resolution = (320, 240)
		self.camera.framerate = 32
		self.rawCapture = PiRGBArray(self.camera, size=(320, 240))

		# variable used to remember the last known face due to frames in
		# which the tracked object was not detected.
		self.old_face = (0,0)

		# sleep to allow the camera capture to initialize
		time.sleep(1)
		
		
	def reduceScene(self, faces):
		# Recognize the face closest the previously detected face.
		if len(faces) > 1:
			closestFace = 0
			minX = 1000
			minY = 1000
			for i, (x, y, w, h) in enumerate(faces):
				if (x - self.old_face[0] < minX) and (y - self.old_face[1] < minY):
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
			
		return (x, y, w, h)
				
				
	def motorControl(self, face_pos, sm, mm, lm):
		# Left movement
		if face_pos[0] > 180:
			self.motor.update_x(sm)
		elif face_pos[0] > 190:
			self.motor.update_x(mm)
		elif face_pos[0] > 200:
			self.motor.update_x(lm)

		# Right movement
		if face_pos[0] < 140:
			self.motor.update_x(-sm)
		elif face_pos[0] < 130:
			self.motor.update_x(-mm)
		elif face_pos[0] < 120:
			self.motor.update_x(-lm)

		# Down movement
		if face_pos[1] > 140:
			self.motor.update_y(sm)
		elif face_pos[1] > 150:
			self.motor.update_y(mm)
		elif face_pos[1] > 160:
			self.motor.update_y(lm)

		# Up movement
		if face_pos[1] < 100:
			self.motor.update_y(-sm)
		elif face_pos[1] < 90:
			self.motor.update_y(-mm)
		elif face_pos[1] < 80:
			self.motor.update_y(-lm)
					
					
	def findObjects(self):
		"""
		The main loop which loops over every incoming video frame. Each frame gets
		processed to find the location of the object and draw a rectangle around
		it.
		"""

		# Don't know where the face starts
		prev_orientation = -1

		for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
			
			# return a list of faces.
			analyzedData = self.analyzeFrame(frame, prev_orientation)
			faces = analyzedData[0]
			flippedFrame = analyzedData[1]
			prev_orientation = analyzedData[2]

			# Draw a rectangle around the faces
			(x, y, w, h) = self.reduceScene(faces)

			# if a face was detected then print the location
			# and update motor(s)
			if x != -1:
				face_pos = (w/2+x,h/2+y)
				self.old_face = face_pos
				print "Center of face: (%s,%s)" % (face_pos[0],face_pos[1])

				self.motorControl(face_pos, SM, MM, LM)

				cv2.rectangle(flippedFrame, (x, y), (x+w, y+h), (0,255,0), 2)


			# Display the resulting frame
			cv2.imshow('Video', flippedFrame)

			self.rawCapture.truncate(0)
			
			#time.sleep(0.25)
			
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

				
	def analyzeFrame(self,frame,prev_orientation=-1):
		"""
		Takes a frame and first rotates based on the physical camera's orientation.
		Converts the frame to greyscale and then uses the Haar cascade to get the
		list of detected objects (faces).
		"""
		# Resize and flip frame for better performance
		if type(frame) is str:
			flippedFrame = cv2.flip(cv2.imread(frame),0)
		else:
			flippedFrame = cv2.flip(frame.array, 0)

		greyscaleFrame = cv2.cvtColor(flippedFrame, cv2.COLOR_BGR2GRAY)

		found_face = False

		# 0 for front, 1 for right side of face, 2 for left side, -1 for nothing
		if not found_face and (prev_orientation == -1 or prev_orientation == 0):		
			faces = self.frontal_classifier.detectMultiScale(
				greyscaleFrame,
				scaleFactor = 1.3, 
				minNeighbors = 5,
				minSize = (15, 15),
				flags = cv2.CASCADE_SCALE_IMAGE
			)
			if len(faces):
				prev_orientation = 0
				found_face = True

		if not found_face and (prev_orientation == -1 or prev_orientation == 1):
			faces = self.profile_classifier.detectMultiScale(
                                greyscaleFrame,
                                scaleFactor = 1.3, 
                                minNeighbors = 5,
                                minSize = (15, 15),
                                flags = cv2.CASCADE_SCALE_IMAGE
                        )
			if len(faces):
				prev_orientation = 1
				found_face = True

		if not found_face and (prev_orientation == -1 or prev_orientation == 2):
			cv2.flip(greyscaleFrame, 1, greyscaleFrame)
			faces = self.profile_classifier.detectMultiScale(
                                greyscaleFrame,
                                scaleFactor = 1.3, 
                                minNeighbors = 5,
                                minSize = (15, 15),
                                flags = cv2.CASCADE_SCALE_IMAGE
                        )
			if len(faces):
				prev_orientation = 2
				found_face = True

		if not found_face:
			faces = ()
			prev_orientation = -1
		

		return (faces,flippedFrame,prev_orientation)
				
