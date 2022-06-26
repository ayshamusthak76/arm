
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
#b 2021
# 

# Import standard python modules.
import sys                                                                                                                                                                                             

# Import blinka python modules.
import board
import digitalio

import Servo_control as sc
import sonic_arm as sa
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
FEED_ID1 = 'digital'
FEED_ID2 = 'hi'


# relay = digitalio.DigitalInOut(board.D5)
# relay.direction = digitalio.Direction.OUTPUT

# def homestate(pwm):

#     # if dist ==1:
#     print("home")
#     sc.move_servo(pwm, 4, 170)
#     sc.move_servo(pwm, 5, 185) #find the values here
#     sc.move_servo(pwm, 6, 230)
    
#     sc.move_servo(pwm, 7, 120)
#     sc.move_servo(pwm, 8, 70)
#     sc.move_servo(pwm, 9, 0)  

def wave(pwm):
    print("wave")
    sc.move_servo(pwm, 4, 170)
    sc.move_servo(pwm, 5, 185) #find the values here
    sc.move_servo(pwm, 6, 230)
    
    sc.move_servo(pwm, 7, 200)
    sc.move_servo(pwm, 8, 40)
    sc.move_servo(pwm, 8, 140)
    sc.move_servo(pwm, 4, 200)
    # sc.move_servo(pwm, 9, 180)  


# Define callback functions which will be called when certain events happen.
def connected(client):
    # Subscribe to changes on a feed named Counter.
    print('Subscribing to Feed {0}'.format(FEED_ID1))
    client.subscribe(FEED_ID1)
    client.subscribe(FEED_ID2)
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
        sa.home(pwm)

    if payload == "Reset":
        print("Taking robot to home")
        wave(pwm)
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