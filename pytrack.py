import sys
sys.path.append('/usr/local/lib/python2.7/site-packages/cv2.so')
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import RPi.GPIO as GPIO
from motor import Motor

class ImageProcessor:
	def __init__(self, cascadePath='cascade/haarcascade_frontalface_default.xml',gpioX=18,gpioY=23):
		self.haarCascade = cv2.CascadeClassifier(cascadePath)
		self.motor = Motor(320,240,53.50,41.41,gpioX,gpioY)

	def findObjects(self):
		center_pos = (160,140)

		camera = PiCamera()
		camera.resolution = (320, 240)
		camera.framerate = 32
		rawCapture = PiRGBArray(camera, size=(320, 240))

		time.sleep(1)
		loop = 0

		for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
			
			analyzedData = self.analyzeFrame(frame)
			faces = analyzedData[0]
			flippedFrame = analyzedData[1]

			# Draw a rectangle around the faces
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
			


			if x != -1:
				face_pos = (w/2+x,h/2+y)
				print "Center of face: (%s,%s)" % (face_pos[0],face_pos[1])

				# Left movement
				if face_pos[0] > 180:
					self.motor.update(5,0)
				elif face_pos[0] > 190:
					self.motor.update(7,0)
				elif face_pos[0] > 200:
					self.motor.update(9,0)
		
				# Right movement
				if face_pos[0] < 140:
					self.motor.update(-5,0)
				elif face_pos[0] < 130:
					self.motor.update(-7,0)
				elif face_pos[0] < 120:
					self.motor.update(-9,0)

				cv2.rectangle(flippedFrame, (x, y), (x+w, y+h), (0,255,0), 2)


			# Display the resulting frame
			cv2.imshow('Video', flippedFrame)

			rawCapture.truncate(0)
			
			#time.sleep(0.25)
			
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

	def analyzeFrame(self,frame):
		# Resize and flip frame for better performance
		if type(frame) is str:
			flippedFrame = cv2.flip(cv2.imread(frame),0)
		else:
			flippedFrame = cv2.flip(frame.array, 0)

		greyscaleFrame = cv2.cvtColor(flippedFrame, cv2.COLOR_BGR2GRAY)

		faces = self.haarCascade.detectMultiScale(
			greyscaleFrame,
			scaleFactor = 1.3, 
			minNeighbors = 5,
			minSize = (15, 15),
			flags = cv2.CASCADE_SCALE_IMAGE
		)

		

		return (faces,flippedFrame)
				
