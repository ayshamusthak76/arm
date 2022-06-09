import cv2 as cv
import numpy as np
import serial
import math


from PIL import Image
import argparse
import time
import serial
import math
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

cap = cv.VideoCapture(0)

whT = 320
confThreshold =0.5
nmsThreshold= 0.2
angle=0


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
classesFile = "RPI/coco.names"
classNames = []

with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')
print(classNames)
## Model Files
modelConfiguration = "RPI/yolov3-tiny.cfg"
modelWeights = "RPI/yolov3-tiny.weights"

net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

def findObjects(outputs,img):

	global count, inputDistance,inputAngle, angle

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
			
		if calcDistance >= 328 and calcDistance <= 352:
			inputDistance = ' 3'
			
		# if object is between middle and biggest circle
		
		if calcDistance >= 353 and calcDistance <= 377:
			inputDistance = ' 4'

		# if obejct is close to the biggest circle
		if calcDistance >= 378:
			inputDistance = ' 5'

		# calculate angle of object to arm
		angle = int(math.atan((centerY - 445)/(centerX - 275 +1))*180/(math.pi+1))

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
    outputNames = [(layersNames[i - 1]) for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(outputNames)
	# outputNames = [(layersNames[i - 1]) for i in net.getUnconnectedOutLayers()]

# 	outputs = net.forward(outputNames)
    
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
            if count >= 5 and done == 1 and angle != 0:
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



























# # This code will detect the location of different recycle materials and communicate
# # with the Arduino (used to control the robotic arm) to pick up and drop the 
# # object in the proper location based on its material.

# # USAGE
# # python recycle_detection.py --recycle_ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03/detect_edgetpu.tflite --labels recycle_ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03/labels.txt

# # import the necessary packages
# # from edgetpu.detection.engine import DetectionEngine
# # from imutils.video import FPS
# # from imutils.video import VideoStream
# from PIL import Image
# import argparse
# # import imutils
# import time
# import cv2 as cv
# import serial
# import math
# import warnings
# import numpy as np
# # filter out RuntimeWarning from a divide by zero error in angle calculation 
# warnings.filterwarnings("ignore", category=RuntimeWarning)

# # stop is used to reset the counting variables
# stop = 0

# cap = cv.VideoCapture(0)

# # count variables used to track the number of imgs detected of each object
# # cardboardCount = 0
# # glassCount = 0
# # metalCount = 0
# # paperCount = 0
# # plasticCount = 0

# # variables used to send to Arduino about location of object
# inputDistance = ' 0'
# inputAngle = ' 90'

# # create variables to connect the RPI to Arduino via USB
# port = "/dev/ttyACM0"
# rate = 9600

# # start the serial communication
# s1 = serial.Serial(port,rate)
# s1.flushInput()

# # done is used to tell program that the arm is done moving
# done = 1

# # list of strings that the Arduino will send to RPI
# comp_list=["Done Moving\r\n","Connected to Arduino\r\n"]


# whT = 320
# confThreshold =0.5
# nmsThreshold= 0.2

# #### LOAD MODEL
# ## Coco Names
# classesFile = "/home/pi/Trash_Sorting_Robot-master/RPI/coco.names"
# classNames = []

# with open(classesFile, 'rt') as f:
#     classNames = f.read().rstrip('\n').split('\n')
# print(classNames)
# ## Model Files
# modelConfiguration = "RPI/yolov3-tiny.cfg"
# modelWeights = "RPI/yolov3-tiny.weights"

# net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
# net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
# net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# # construct the argument parser and parse the arguments
# # ap = argparse.ArgumentParser()
# # # ap.add_argument("-m", "--model", required=True,
# # # 	help="path to TensorFlow Lite object detection model")
# # ap.add_argument("-l", "--labels", required=True,
# # 	help="path to labels file")
# # ap.add_argument("-c", "--confidence", type=float, default=0.3,
# # 	help="minimum probability to filter weak detections")
# # args = vars(ap.parse_args())

# # initialize the labels dictionary
# print("[INFO] parsing class labels...")
# labels = {}

# # # loop over the class labels file
# # for row in open(args["labels"]):
# # 	# unpack the row and update the labels dictionary
# # 	(classID, label) = row.strip().split(maxsplit=1)
# # 	labels[int(classID)] = label.strip()

# # load the Google Coral object detection model
# # print("[INFO] loading Coral model...")
# # model = DetectionEngine(args["model"])

# # initialize the video stream and allow the camera sensor to warmup,
# # and initialize the FPS counter
# print("[INFO] starting video stream...")
# # vs = VideoStream(src=0).start()
# #vs = VideoStream(usePiCamera=False).start()
# time.sleep(5)
# # fps = FPS().start()

# with open(classesFile, 'rt') as f:
#     classNames = f.read().rstrip('\n').split('\n')

# def findObjects(outputs,img):
# 	hT, wT, cT = img.shape
# 	bbox = []
# 	classIds = []
# 	confs = []
# 	for output in outputs:
# 		for det in output:
# 			scores = det[5:]
# 			classId = np.argmax(scores)
# 			confidence = scores[classId]
# 			if confidence > confThreshold:
# 				w,h = int(det[2]*wT) , int(det[3]*hT)
# 				x,y = int((det[0]*wT)-w/2) , int((det[1]*hT)-h/2)
# 				bbox.append([x,y,w,h])
# 				classIds.append(classId)
# 				confs.append(float(confidence))

# 	indices = cv.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)

# 	for i in indices:
# 		# i = i[0]
# 		box = bbox[i]
# 		x, y, w, h = box[0], box[1], box[2], box[3]
# 		# print(x,y,w,h)
# 		cv.rectangle(img, (x, y), (x+w,y+h), (255, 0 , 255), 2)
# 		cv.putText(img,f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%', (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
		
# 	return indices,bbox,classIds, confs

# # loop over the imgs from the video stream
# while True:
# 	# grab the img from the threaded video stream and resize it
# 	# to have a maximum width of 500 pixels
# 	# img = vs.read()
# 	# img = imutils.resize(img, width=500)
# 	# img = img.copy()
# 	success, img = cap.read()
	
# 	# prepare the img for object detection by converting (1) it
# 	# from BGR to RGB channel ordering and then (2) from a NumPy
# 	# array to PIL image format
# 	blob = cv.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
# 	net.setInput(blob)

# 	layersNames = net.getLayerNames()

# 	outputNames = [(layersNames[i - 1]) for i in net.getUnconnectedOutLayers()]

# 	outputs = net.forward(outputNames)

# 	results,bbox,classIds,confs = findObjects(outputs,img)


# 	# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# 	# img = Image.fromarray(img)

# 	# make predictions on the input img
# 	start = time.time()


# 	# results = model.DetectWithImage(img, threshold=args["confidence"],
# 		# keep_aspect_ratio=True, relative_coord=False) #############################33############
# 	end = time.time()



#     # make three circles indicating the arm's range of motion
# 	cv.circle(img, (275, 445), 390, (0, 0, 255), 3, 8, 0)
# 	cv.circle(img, (275, 445), 365, (0, 0, 255), 3, 8, 0)
# 	cv.circle(img, (275, 445), 340, (0, 0, 255), 3, 8, 0)	
# 	cv.circle(img, (275, 445), 315, (0, 0, 255), 3, 8, 0)
# 	cv.circle(img, (275, 445), 290, (0, 0, 255), 3, 8, 0)

# 	# loop over the results
# 	for r in results:
# 		# extract the bounding box and box and predicted class label
# 		# box = r.bounding_box.flatten().astype("int")
# 		box = bbox[r]
# 		(startX, startY, endX, endY) = box[0], box[1], box[2], box[3]
# 		label = classNames[classIds[r]]

# 		# center coordinates of object detected
# 		centerX = ((endX - startX) // 2) + startX
# 		centerY = ((endY - startY) // 2) + startY

# 		# calculate the distance from arm to object
# 		calcDistance = int(math.sqrt(((centerX - 275)**2)+((centerY - 445)**2)))
			
# 		# if object is close to the smallest circle
# 		if calcDistance <= 302:
# 			inputDistance = ' 1'
# 			print("small circle")

# 		# if object is between smallest and middle circle
# 		if calcDistance >= 303 and calcDistance <= 327:
# 			inputDistance = ' 2'
# 			print("btwn circle")

# 		# if object is close to middle circle
# 		if calcDistance >= 328 and calcDistance <= 352:
# 			inputDistance = ' 3'
# 			print(" circle")

			
# 		# if object is between middle and biggest circle
# 		if calcDistance >= 353 and calcDistance <= 377:
# 			inputDistance = ' 4'
# 			print(" circle")

# 		# if obejct is close to the biggest circle
# 		if calcDistance >= 378:
# 			inputDistance = ' 5'
# 			print(" circle")

# 		# calculate angle of object to arm
# 		angle = int(math.atan((centerY - 445)/(centerX - 275))*180/math.pi)

# 		# calculated angle gives angles between (-90,90) NOT (0,180)
# 		# if statements used to convert the (-90,90) angles to (0,180)
# 		if angle > 0:
# 			angle = abs(angle - 180)

# 		if angle < 0:
# 			angle = -angle
			
# 		if angle == 90: 
# 			angle = 0

# 		# convert (0,180) angle to a string to send to Arduino
# 		inputAngle = ' ' + str(angle)

# 		# create circle of center of object
# 		cv.circle(img, (centerX, centerY), 5, (0, 0, 255), -1)
# 		# reate circle of where the arm is 
# 		cv.circle(img, (275, 370), 5, (0, 0, 255), -1)
	
# 		# reate line connecting the arm and object location with the angle calculated too
# 		cv.line(img, (centerX, centerY), (275, 370), (0, 0, 255), 1)
# 		cv.putText(img, str(angle), (260, 360), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
# 		# reate name and bounding box around object
# 		cv.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0))
# 		y = startY - 15 if startY - 15 > 15 else startY + 15
# 		text = "{}: {:.2f}%".format(label, confs[r] * 100)
# 		cv.putText(img, text, (startX, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)      

	
# 	# if the Arduino sends data to the RPI
# 	if s1.inWaiting()>0:
# 		# take the input and print it
# 		inputValue = s1.readline()
# 		print(inputValue.decode())
# 		# if the Arduino tells RPI that it is done moving
# 		if inputValue.decode() == "Done Moving\r\n":
# 			done = 1
# 		# if the input is in the comp_list
# 		if inputValue.decode() in comp_list:

# 			# plastic has been detected for at least 20 imgs
# 			# if plasticCount >= 20 and done == 1 and angle != 0:
# 			# 	print("Plastic imgs:", plasticCount)
# 			print(inputDistance)
# 			print(inputAngle)
# 			s1.write(bytes('1', 'utf-8'))
# 			s1.write(bytes(' 1 ', 'utf-8'))
# 			s1.write(bytes(inputDistance, 'utf-8'))
# 			s1.write(bytes(inputAngle, 'utf-8'))
# 			stop = 1
# 			done = 0
		
# 		# if stop equals 1 than reset all counting variables
# 		if stop == 1:
# 			cardboardCount = 0
# 			glassCount = 0
# 			metalCount = 0
# 			paperCount = 0
# 			plasticCount = 0
# 			stop = 0
				
# 	# show the output img and wait for a key press
# 	cv.imshow("img", img)
# 	key = cv.waitKey(1) & 0xFF

# 	# if the `q` key was pressed, break from the loop
# 	if key == ord("q"):
# 		break

# 	# update the FPS counter
# # 	fps.update()

# # # stop the timer and display FPS information
# # fps.stop()
# # print("[INFO] elapse time: {:.2f}".format(fps.elapsed()))
# # print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# # do a bit of cleanup
# cv.destroyAllWindows()
# # vs.stop()
