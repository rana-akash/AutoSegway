from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import argparse
import imutils
import numpy as np
import RPi.GPIO as gpio

left_motor_pin = 17
right_motor_pin = 18

gpio.setmode(gpio.BCM)


gpio.setup(left_motor_pin,gpio.OUT)
gpio.setup(right_motor_pin,gpio.OUT)
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 3
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(2.0)
starttime = time.time()
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    frame = frame.array
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > args["confidence"]:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            
            (startX, startY, endX, endY) = box.astype("int")
            label = "{}: {:.2f}%".format(CLASSES[idx],confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY),COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            if "bottle" in label:
                print('bottle detected')
                gpio.output(left_motor_pin,gpio.LOW)
                gpio.output(right_motor_pin,gpio.LOW)
                starttime = time.time()
            print(time.time() - starttime)
            if ("bottle" not in label) and ((time.time() - starttime) > 5):
                print('stopping motors')
                gpio.output(left_motor_pin,gpio.HIGH)
                gpio.output(right_motor_pin,gpio.HIGH)
                #time.sleep(2)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    rawCapture.truncate(0)
cv2.destroyAllWindows()
            
