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

# sc.move_servo(pwm,9, 0) #gripper open
# sc.move_servo(pwm, 4, 135)
# #set
# sc.move_servo(pwm,5, 70) # increase - goes back // 0 is the most forward
# sc.move_servo(pwm, 6, 200) # increase - goes forward
# sc.move_servo(pwm,7, 100)
# sc.move_servo(pwm,8, 80)
# sc.move_servo(pwm,9, 45)
# sc.move_servo(pwm,9, 45)
# sc.move_servo(pwm,9, 270)
# for i in range (0,270, 20):
#     sc.move_servo(pwm,6, i)  
# 
# sc.move_servo(pwm,9, 0)
# sc.move_servo(pwm, 4, 135)
# #set
# sc.move_servo(pwm,5, 70)
# sc.move_servo(pwm, 6, 200)
# sc.move_servo(pwm,7, 100)
# sc.move_servo(pwm,8, 80)
# sc.move_servo(pwm,9, 180)  

# sc.move_servo(pwm, 4, 135)
# #set
# sc.move_servo(pwm,5, 160)
# sc.move_servo(pwm, 6, 230)
# sc.move_servo(pwm,7, 100)
# sc.move_servo(pwm,8, 80)
# sc.move_servo(pwm,9, 45)


# print('home')
# sc.move_servo(pwm, 4, 135)
# sc.move_servo(pwm,5, 160)
# sc.move_servo(pwm, 6, 200)
# sc.move_servo(pwm,7, 100)
# sc.move_servo(pwm,8, 80
# )
# sc.move_servo(pwm,9, 45)


#pickup
# print("pickup")
# sc.move_servo(pwm,9, 0)
sc.move_servo(pwm, 4, 135)
sc.move_servo(pwm,5, 60)
sc.move_servo(pwm,6, 180)
sc.move_servo(pwm,7, 50)
sc.move_servo(pwm,8, 100)
sc.move_servo(pwm,9, 270)

