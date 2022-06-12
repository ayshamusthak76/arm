import time
# Import the PCA9685 module.
import Adafruit_PCA9685
import Servo_control as sc
import RPi.GPIO as GPIO                    #Import GPIO library
import time

pwm = Adafruit_PCA9685.PCA9685()

print('Set frequency')
# Set the frequency
pwm.set_pwm_freq(sc.SERVO_MOTOR_FREQUENCY)
time.sleep(2)

sc.move_servo(pwm, 4, 135)
#set
sc.move_servo(pwm,5, 160)
sc.move_servo(pwm, 6, 35)
sc.move_servo(pwm,7, 180)
sc.move_servo(pwm,8, 65)
sc.move_servo(pwm,9, 45)