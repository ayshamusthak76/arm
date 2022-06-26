
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

import time
import Adafruit_PCA9685



# relay = digitalio.DigitalInOut(board.D5)
# relay.direction = digitalio.Direction.OUTPUT

def homestate(pwm):

    # if dist ==1:
    print("home")
    sc.move_servo(pwm, 4, 170)
    sc.move_servo(pwm, 5, 185) #find the values here
    sc.move_servo(pwm, 6, 230)
    
    sc.move_servo(pwm, 7, 120)
    sc.move_servo(pwm, 8, 70)
    sc.move_servo(pwm, 9, 0)  


pwm = Adafruit_PCA9685.PCA9685()

print('Set frequency')
pwm.set_pwm_freq(sc.SERVO_MOTOR_FREQUENCY)


homestate(pwm)
