
import cv2
import numpy as np
import RPi.GPIO as GPIO
import arm as sa
import Adafruit_PCA9685
import Servo_control as sc
# in1 = 4
in1=20
# in2 = 17
in2 = 16

in3 = 27
in4 = 22
en1 = 19
en2 = 26
# en2 = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(en1, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
p1 = GPIO.PWM(en1, 100)
p2 = GPIO.PWM(en2, 100)
p1.start(40)
p2.start(40)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
# pwm = Adafruit_PCA9685.PCA9685()

# print('Set frequency')
# pwm.set_pwm_freq(sc.SERVO_MOTOR_FREQUENCY)


def stopcar():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

while True:

    dist = sa.check_dist1()
    print(dist)
    if dist>30:
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)
    else:
        stopcar()
        print('Stopping car!!!!!!')
        sa.home()
        sa.pickup()
        sa.dropoff()
        sa.home()
        continue

