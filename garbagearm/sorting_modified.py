import cv2 as cv
import numpy as np
import serial
import math

cap = cv.VideoCapture(0)

whT = 320
confThreshold =0.5
nmsThreshold= 0.2


# stop is used to reset the counting variables
stop = 0

# count variables used to track the number of frames detected of each object
count = 0

##defaults 
inputDistance = '0'
inputAngle = '90'

# create variables to connect the RPI to Arduino via USB
port = "/dev/ttyACM0"
rate = 9600

# start the serial communication
s1 = serial.Serial(port,rate)
s1.flushInput()

# done is used to tell program that the arm is done moving
done = 1

# list of strings that the Arduino will send to RPI
comp_list=["Done Moving\r\n","Connected to Arduino\r\n"]

#### LOAD MODEL
## Coco Names
classesFile = "coco.names"
classNames = []

# with open(classesFile, 'rt') as f:
#     classNames = f.read().rstrip('\n').split('\n')
# print(classNames)
## Model Files
modelConfiguration = "yolov3-tiny.cfg"
modelWeights = "yolov3-tiny.weights"

net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_INFERENCE_ENGINE)
net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)

def findObjects(outputs,img):
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w,h = int(det[2]*wT) , int(det[3]*hT)
                x,y = int((det[0]*wT)-w/2) , int((det[1]*hT)-h/2)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))

    indices = cv.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)

    # return indices, bbox, classIds, confs
    for i in indices:
        # i = i[0]
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]

        centerX = ((w - x) // 2) + x
        centerY = ((h - y) // 2) + y

        calcDistance = int(math.sqrt(((centerX - 275)**2)+((centerY - 445)**2)))

		# if object is close to the smallest circle
        if calcDistance <= 302:
            inputDistance = ' 1'

        # if object is between smallest and middle circle
        if calcDistance >= 303 and calcDistance <= 327:
            inputDistance = ' 2'
            
        # if object is close to middle circle
        if calcDistance >= 328 and calcDistance <= 352:
            inputDistance = ' 3'
            
        # if object is between middle and biggest circle
        if calcDistance >= 353 and calcDistance <= 377:
            inputDistance = ' 4'

        # if obejct is close to the biggest circle
        if calcDistance >= 378:
            inputDistance = ' 5'

        # calculate angle of object to arm
        angle = int(math.atan((centerY - 445)/(centerX - 275))*180/math.pi)

        # calculated angle gives angles between (-90,90) NOT (0,180)
        # if statements used to convert the (-90,90) angles to (0,180)
        if angle > 0:
            angle = abs(angle - 180)

        if angle < 0:
            angle = -angle
			
        if angle == 90: 
            angle = 0

		# convert (0,180) angle to a string to send to Arduino
        inputAngle = ' ' + str(angle)

		# create circle of center of object
        cv.circle(img, (centerX, centerY), 5, (0, 0, 255), -1)

		# create circle of where the arm is 
        cv.circle(img, (275, 370), 5, (0, 0, 255), -1)

        cv.line(img, (centerX, centerY), (275, 370), (0, 0, 255), 1)
        cv.putText(img, str(angle), (260, 360), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
      
        # print(x,y,w,h)
        cv.rectangle(img, (x, y), (x+w,y+h), (255, 0 , 255), 2)
        label = classNames[classIds[i]]
        cv.putText(img,f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%',
                  (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

        if done==1:
            if label in classNames:
                count+=1
    return angle, inputAngle, inputDistance, count

while True:
    success, img = cap.read() 
    
    blob = cv.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
    net.setInput(blob)
    layersNames = net.getLayerNames()
    outputNames = [(layersNames[i[0] - 1]) for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(outputNames)
    
	# draw alignment circles
    cv.circle(img, (275, 445), 390, (0, 0, 255), 3, 8, 0)
    cv.circle(img, (275, 445), 365, (0, 0, 255), 3, 8, 0)
    cv.circle(img, (275, 445), 340, (0, 0, 255), 3, 8, 0)	
    cv.circle(img, (275, 445), 315, (0, 0, 255), 3, 8, 0)
    cv.circle(img, (275, 445), 290, (0, 0, 255), 3, 8, 0)
    # cv.circle(img, (275, 0), 5, (0, 0, 255), 3, 8, 0)

    angle, inputAngle, inputDistance, count = findObjects(outputs,img)
    
    if s1.inWaiting()>0:
        # take the input and print it
        inputValue = s1.readline()
        print(inputValue.decode())
        # if the Arduino tells RPI that it is done moving
        if inputValue.decode() == "Done Moving\r\n":
            done = 1
        # if the input is in the comp_list
        if inputValue.decode() in comp_list:
            # cardboard has been detected for at least 20 frames
            if count >= 20 and done == 1 and angle != 0:
                print("Frames:", count)
                print(inputDistance)
                print(inputAngle)
                s1.write(bytes('1', 'utf-8'))
                s1.write(bytes(' 1', 'utf-8'))
                s1.write(bytes(inputDistance, 'utf-8'))
                s1.write(bytes(inputAngle, 'utf-8'))
                stop = 1
                done = 0
        
        if stop == 1:
            count = 0
            stop=0
			

    cv.imshow('Image', img)
    # cv.waitKey(1)
    key = cv.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break