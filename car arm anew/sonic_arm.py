
import Adafruit_PCA9685
import Servo_control as sc
import RPi.GPIO as GPIO                    #Import GPIO library
import time
#Import time library
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)   

TRIG = 23
ECHO = 24


GPIO.setup(TRIG,GPIO.OUT)                  # initialize GPIO Pin as outputs
GPIO.setup(ECHO,GPIO.IN)                   # initialize GPIO Pin as input


time.sleep(5)

def home(pwm):
    print('home')
    sc.move_servo(pwm, 4, 135)
    sc.move_servo(pwm,5, 100)
    sc.move_servo(pwm, 6, 200)
    sc.move_servo(pwm,7, 80)
    sc.move_servo(pwm,8, 80)
    sc.move_servo(pwm,9, 45)

def wave(pwm):
    print('wave')
    sc.move_servo(pwm, 4, 170)
    sc.move_servo(pwm, 5, 185) #find the values here
    sc.move_servo(pwm, 6, 230)
    
    sc.move_servo(pwm, 7, 290)
    sc.move_servo(pwm, 8, 40)
    sc.move_servo(pwm, 8, 140)
    sc.move_servo(pwm, 4, 200)
    sc.move_servo(pwm, 8, 40)
    sc.move_servo(pwm, 8, 140)

def pickup(pwm):
    print('pickup')
    sc.move_servo(pwm,9, 0)
    sc.move_servo(pwm, 4, 135)
    sc.move_servo(pwm,5, 60)
    sc.move_servo(pwm,6, 180)
    sc.move_servo(pwm,7, 50)
    sc.move_servo(pwm,8, 100)
    sc.move_servo(pwm,9, 270)

def dropoff(pwm):
    print('dropoff')
    sc.move_servo(pwm, 4, 45)
    sc.move_servo(pwm,9, 0)
    sc.move_servo(pwm, 5, 185) 
    sc.move_servo(pwm, 6, 230)    
    sc.move_servo(pwm,9, 270)

def check_dist():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    StartTime = 0
    StopTime = 5
    ct=0
    while GPIO.input(ECHO) == 0:
        StartTime = time.time()
        ct+=1
        if ct>5000:
            return(0)
    while GPIO.input(ECHO) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance

def check_dist1():

##############3
    i=0
    avgDistance=0
    for i in range(5):
        GPIO.output(TRIG, False)                 #Set TRIG as LOW
        time.sleep(0.1)                                   #Delay

        GPIO.output(TRIG, True)               
        time.sleep(0.00001)                        
        GPIO.output(TRIG, False)               
        while GPIO.input(ECHO)==0:               
            pulse_start = time.time()
        print("out1")
        while GPIO.input(ECHO)==1:          
            pulse_end = time.time()
        print("out")
        time.sleep(0.5)
        pulse_duration = pulse_end - pulse_start 
        distance = pulse_duration * 17150        
        distance = round(distance,2)                 
        avgDistance=avgDistance+distance

    avgDistance=avgDistance/5
    print (avgDistance)
    return avgDistance
    # flag=061
    #     home()

if __name__ == "__main__":

    pwm = Adafruit_PCA9685.PCA9685()

    print('Set frequency')
    # Set the frequency
    pwm.set_pwm_freq(sc.SERVO_MOTOR_FREQUENCY)
    time.sleep(2)
    home(pwm)
    # wave(pwm)
    while True:
        print(check_dist())
        dist = check_dist()
        print(dist)
        if dist < 26:
            pickup(pwm)
            dropoff(pwm)
            home(pwm)
            time.sleep(5)

        
        # pickup(pwm, 14)
        # print("pickup 1 done")
        # time.sleep(5)
        # sc.move_servo(pwm,5, 160)
        # sc.move_servo(pwm, 6, 200)
        # pickup(pwm, 19)
        # time.sleep(5)
        # sc.move_servo(pwm,5, 160)
        # sc.move_servo(pwm, 6, 200)
        # print("pickup 2 done")
        # pickup(pwm, 24)
        # time.sleep(5)
        