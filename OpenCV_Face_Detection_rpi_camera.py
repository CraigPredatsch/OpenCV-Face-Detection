import io
import time
import picamera
import cv2
import numpy
import sys
sys.path.append('/usr/local/lib/python3.4/site-packages')

#Create a memory stream so photos doesn't need to be saved in a file
stream = io.BytesIO()

#Stream video to the screen for 5 seconds so that a person can align themselves in front of the camera
#Capture image
with picamera.PiCamera() as camera:
    camera.resolution = (1920, 1080)
    camera.start_preview()
    time.sleep(5)
    camera.capture(stream, 'jpeg')

#Convert the picture into a numpy array
buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)


#Now creates an OpenCV image
image = cv2.imdecode(buff, 1)

#Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier('/home/pi/frontal_face_default.xml')
if face_cascade.empty(): raise Exception("Face Casecade empty. Is the path correct?")

eye_cascade = cv2.CascadeClassifier('/home/pi/eye.xml')
if eye_cascade.empty(): raise Exception("Eye cascade is empty. Is the path correct>")

#Convert to grayscale
#gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

#Look for faces in the image using the loaded cascade file
faces = face_cascade.detectMultiScale(image, 1.1, 5)

print "Found "+str(len(faces))+" face(s)"

#Draw a blue rectangle around every found face
for (x,y,w,h) in faces:
    cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)

    eyes = eye_cascade.detectMultiScale(image)              #Look for eyes within the rectangles drawn around faces using the loaded cascade file
    print "Found "+str(len(eyes))+" eye(s)"
    for(ex, ey, ew, eh) in eyes:                                #Draw a green rectangle around each eye
        cv2.rectangle(image, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

#Save the result image
cv2.imwrite('result.jpg',image)
