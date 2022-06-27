
# 
# References:
# – https://learn.adafruit.com/welcome-to-adafruit-io/client-library
# – https://github.com/adafruit/Adafruit_IO_Python/blob/master/examples/basics/subscribe.py
# 
# Hardware
# – Raspberry Pi 4 Model B
#   [2GB] https://my.cytron.io/p-raspberry-pi-4-model-b-2gb?tracking=idris
#   [4GB] https://my.cytron.io/p-raspberry-pi-4-model-b-4gb?tracking=idris
#   [8GB] https://my.cytron.io/p-raspberry-pi-4-model-b-8gb-latest?tracking=idris
# – Grove Base Kit for Raspberry Pi
#   https://my.cytron.io/p-grove-base-kit-for-raspberry-pi?tracking=idris
# 
# Install
# – sudo pip3 install adafruit-blinka
# – sudo pip3 install adafruit-io
# 
# Update:
# 28 Feb 2021
# 

# Import standard python modules.
import sys

# Import blinka python modules.
import board
import digitalio

import ServoControl as sc

import time
import Adafruit_PCA9685


# This example uses the MQTTClient instead of the REST client
from Adafruit_IO import MQTTClient

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'aio_UMHC52Vofbb6a44TCTj3BrD2umxi'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'rasheedarasool'

# Set to the ID of the feed to subscribe to for updates.
FEED_ID = 'digital'

relay = digitalio.DigitalInOut(board.D5)
relay.direction = digitalio.Direction.OUTPUT

def homestate(pwm):
    sc.move_servo(pwm,4,120)
    time.sleep(3)
    sc.move_servo(pwm,5,200)
    time.sleep(3)
    sc.move_servo(pwm,6,230)
    time.sleep(3)
    sc.move_servo(pwm,7,150)
    time.sleep(3)
    sc.move_servo(pwm,8,60)
    time.sleep(3)
    sc.move_servo(pwm,9,120)
    time.sleep(3)

# Define callback functions which will be called when certain events happen.
def connected(client):
    """Connected function will be called when the client is connected to
    Adafruit IO.This is a good place to subscribe to feed changes.  The client
    parameter passed to this function is the Adafruit IO MQTT client so you
    can make calls against it easily.
    """
    # Subscribe to changes on a feed named Counter.
    print('Subscribing to Feed {0}'.format(FEED_ID))
    client.subscribe(FEED_ID)
    print('Waiting for feed data…')

def disconnected(client):
    """Disconnected function will be called when the client disconnects."""
    sys.exit(1)

def message(client, feed_id, payload):
    """Message function will be called when a subscribed feed has a new value.
    The feed_id parameter identifies the feed, and the payload parameter has
    the new value.
    """
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    
    if payload == "ON":
        print("Taking robot to home")
        homestate(pwm)
        # relay.value = False
# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
pwm = Adafruit_PCA9685.PCA9685()

print('Set frequency')
pwm.set_pwm_freq(sc.SERVO_MOTOR_FREQUENCY)
# Setup the callback functions defined above.
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message

# Connect to the Adafruit IO server.
client.connect()

# The first option is to run a thread in the background so you can continue
# doing things in your program.
client.loop_blocking()

###########################################BLYNK CODE###################################

import numpy as np #Used for processing image data
import cv2 as cv2 #Used for capturing images with the webcam
from PIL import Image, ImageEnhance, ImageOps #Used for processing image data
import time #Used for an FPS counter
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D #Import various layers for the Neural Net
from tensorflow.keras.models import Sequential #Import libraries for the Neural Net
from tensorflow.keras.optimizers import Adam  #Import optimizers for the Neural Net
import tensorflow as tf #import Tensorflow
from tensorflow.keras.models import model_from_json #Import tensorflow file saving
import blynklib #Import Blynk library
# import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
import ServoControl as sc

import time
# Import the PCA9685 module.
import Adafruit_PCA9685

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
# motor1 = 13 #GPIO Pin for motor1
# motor2 = 12 #GPIO Pin for motor2

servo1 = 0
servo2 = 1
servo3 = 2
servo4 = 3
servo5 = 4
servo6 = 5

# GPIO.setup(motor1, GPIO.OUT)
# GPIO.setup(motor2, GPIO.OUT)
# motor1Servo = GPIO.PWM(motor1, 50) #Set Motors to PWM. Change this depeneding on how your motor controller works
# motor1Servo.start(8)
# motor2Servo = GPIO.PWM(motor2, 50) #Set Motors to PWM. Change this depeneding on how your motor controller works
# motor2Servo.start(8)
# motor1Servo.ChangeDutyCycle(7.5) #Had to change duty cycle twice due to a strange bug with my RPI
# motor2Servo.ChangeDutyCycle(7.5) #Had to change duty cycle twice due to a strange bug with my RPI

def servoControl(pwm, pin, value): #Change this function to be apprpriate for your robot and motor controllers
    # motor1Servo.ChangeDutyCycle(7.5 + value) # I used this calculation due to tank steering
    # motor2Servo.ChangeDutyCycle(7.5 - value)
    # value = sc.convert_angle_to_pwm_board_step(value)
    # print("blynk value",value)
    # val = int(((value+1)*135)+1)
    # print("angle", val)
    print("servo control beg")
    sc.move_servo(pwm,pin,int(value))
    time.sleep(3)
    print("servo control end ")
    

# We sleep in the loops to give the servo time to move into position.
# for i in range(180):
#     servo7.angle = i
#     time.sleep(0.03)
# for i in range(180):
#     servo7.angle = 180 - i
#     time.sleep(0.03)

# You can also specify the movement fractionally.
# fraction = 0.0
# while fraction < 1.0:
#     servo7.fraction = fraction
#     fraction += 0.01
#     time.sleep(0.03)

# pca.deinit()

def aicontrol(action,pwm):
    for i in range(6):
        sc.move_servo(pwm,i,action[i])

class Agent:
    def __init__(self):
        self.userSteering = [0,0,0,0,0,0]
        self.aiMode = False
        self.model = Sequential([ #This is the actual Neural net
            Conv2D(32, (7,7), input_shape=(240, 320, 3),
                   strides=(2, 2), activation='relu', padding = 'same'),
            MaxPooling2D(pool_size=(5,5), strides=(2, 2), padding= 'valid'),
            Conv2D(64, (4, 4), activation='relu', strides=(1, 1), padding = 'same'),
            MaxPooling2D(pool_size=(4,4), strides=(2,2), padding= 'valid'),
            Conv2D(128, (4,4), strides=(1, 1), activation='relu', padding = 'same'),
            MaxPooling2D(pool_size=(5, 5), strides=(3, 3),padding = 'valid'),
            Flatten(),
            Dense(384, activation='relu'),
            Dense(64, activation="relu", name="layer1"),
            Dense(8, activation="relu", name="layer2"),
            Dense(6, activation="linear", name="layer3"),
        ])
        self.model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.05))
        #self.model.load_weights("selfdrive.h5") # use this to import your pretrained weights
        # print(self.model.summary()) # use this to get a summary of the CNN
        self.cap = cv2.VideoCapture(0) # This controls which camera device is used. You might need to tweak this based on your camera
        self.cap.set(3, 320) # This controls the camera's resolution. You might need to tweak this based on your camera. 
        self.cap.set(4, 240) # This controls the camera's resolution. You might need to tweak this based on your camera


    # def act(self, state): #This method is for the AI behaving in autonomous mode
    #     state = np.reshape(state, (1, 240, 320, 3))
    #     # action = self.model.predict(state)[0][0]
    #     # action = (action * 2) - 1
    #     actionset = self.model.predict(state)[0] ############CHANGE THIS AND MAYBE THE STATE ALSO BECAUSE OF THAT
    #     print(actionset)
    #     actionset = np.array(list((i*2)-1 for i in actionset))
    #     aicontrol(action,pwm)
    #     return action

    def learn(self, state, action): #This method is where the AI's Neural net improves/learns
        state = np.reshape(state, (1, 240,320,3))
        history = self.model.fit(np.array(state), np.array([action]), batch_size=1, epochs=1, verbose=0)
        # print("LOSS: ", history.history.get("loss")[0])
 
    # def getState(self):
    #     ret, frame = self.cap.read() # This gets the actual Webcam Image
    #     pic = np.array(frame) #Convert it to a NP array
    #     cv2.imshow('Image', frame)
    #     processedImg = np.reshape(pic, (240, 320, 3)) / 255 #reshape it
        
        # return processedImg 

    # def observeAction(self):
    #     # return (self.userSteering + 1) / 2
    #     return np.array(list((i+1)/2 for i in self.userSteering))

agent = Agent() 
BLYNK_AUTH = 'PytggOT62RhJT6BAc5Qj1q1DzV-4VmNk' #insert your blynk code from your blynk project
blynk = blynklib.Blynk(BLYNK_AUTH)

@blynk.handle_event('write V4') # We used pin v4 on the blynk app for steering control. Hence 'write V4'
def write_virtual_pin_handler(pin, value):
    print("Servo1 value: ",float(value[0])) 
    agent.userSteering[0] = float(value[0]) #updates the AI's memory of steering angle
    servoControl(pwm, pin, float(value[0])) #changes the motors to appropriately turn based on the steering input

@blynk.handle_event('write V5') # We used pin v4 on the blynk app for steering control. Hence 'write V4'
def write_virtual_pin_handler(pin, value):
    print("Servo2 value: ",float(value[0])) 
    agent.userSteering[1] = float(value[0]) #updates the AI's memory of steering angle
    servoControl(pwm, pin, float(value[0])) #changes the motors to appropriately turn based on the steering input

@blynk.handle_event('write V6') # We used pin v4 on the blynk app for steering control. Hence 'write V4'
def write_virtual_pin_handler(pin, value):
    print("Servo3 value: ",float(value[0])) 
    agent.userSteering[2] = float(value[0]) #updates the AI's memory of steering angle
    servoControl(pwm, pin, float(value[0])) #changes the motors to appropriately turn based on the steering input

@blynk.handle_event('write V7') # We used pin v4 on the blynk app for steering control. Hence 'write V4'
def write_virtual_pin_handler(pin, value):
    print("Servo4 value: ",float(value[0])) 
    agent.userSteering[3] = float(value[0]) #updates the AI's memory of steering angle
    servoControl(pwm, pin, float(value[0])) #changes the motors to appropriately turn based on the steering input

@blynk.handle_event('write V8') # We used pin v4 on the blynk app for steering control. Hence 'write V4'
def write_virtual_pin_handler(pin, value):
    print(" Servo5 value: ",float(value[0])) 
    agent.userSteering[4] = float(value[0]) #updates the AI's memory of steering angle
    servoControl(pwm, pin, float(value[0])) #changes the motors to appropriately turn based on the steering input

@blynk.handle_event('write V9') # We used pin v4 on the blynk app for steering control. Hence 'write V4'
def write_virtual_pin_handler(pin, value):
    print("Servo6 value: ",float(value[0]),pin) 
    agent.userSteering[5] = float(value[0]) #updates the AI's memory of steering angle
    servoControl(pwm, pin, float(value[0])) #changes the motors to appropriately turn based on the steering input

@blynk.handle_event('write V0') # We used pin v2 on the blynk app for autonomous/learning control. Hence 'write V2'
def write_virtual_pin_handler(pin, value):
    agent.aiMode = False if value == 1 else True 
    # change the AI's mode based on the reading 

# @blynk.handle_event('write v*')
# def call_wild_card(pin,value):
#     print("Reading slider values")
#     print(pin, value)    
# @blynk.handle_event('write V1') # We used pin v2 on the blynk app for autonomous/learning control. Hence 'write V2'
# def write_virtual_pin_handler(pin, value):
#     if value == 1:
#         record()
         #change the AI's mode based on the reading 



if __name__ == "__main__":
    
    print('Initialize PWM board controller')
    # Initialise the PCA9685 using the default address (0x40).
    pwm = Adafruit_PCA9685.PCA9685()

    print('Set frequency')
    # Set the frequency
    pwm.set_pwm_freq(sc.SERVO_MOTOR_FREQUENCY)
    counter = 0
    while True:
        # if counter ==0:
        #     for i in range(6):
        #         homestate(pwm)
        #         counter+=1
        #         time.sleep(5)
            
        blynk.run()
        
        # if agent.aiMode == False: #This is the AI's Learning mode
        #     start = time.time()
        #     state = agent.getState()
        #     action = agent.observeAction()
        #     counter += 1
        #     if counter % 1 == 0: # you can change this so the AI doesn't learn every iteration
        #         start = time.time()
        #         agent.learn(state, action)
        #         agent.memory = []
        #     if counter % 50 == 0: #change this to how often you want your AI to save its weights
        #        agent.model.save_weights("selfdrive.h5")
        #     # print("framerate: ", 1/(time.time() - start))
        #     # write_virtual_pin_handler(4)


        # else: 
        #     while agent.aiMode == True: #This is the autonomous loop
        #         start = time.time() 
        #         state = agent.getState()
        #         action = agent.act(state)
        #         print("action", action)
        #         print("framerate: ", 1/(time.time() - start))
        
        key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break


