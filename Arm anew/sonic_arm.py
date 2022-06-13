import time
# Import the PCA9685 module.
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
    sc.move_servo(pwm, 4, 135)
    #set
    sc.move_servo(pwm,5, 160)
    sc.move_servo(pwm, 6, 230)
    sc.move_servo(pwm,7, 100)
    sc.move_servo(pwm,8, 80)
    sc.move_servo(pwm,9, 45)

def pickup(pwm):
    sc.move_servo(pwm,9, 0)
    sc.move_servo(pwm, 4, 135)
    #set
    sc.move_servo(pwm,5, 70)
    sc.move_servo(pwm, 6, 200)
    sc.move_servo(pwm,7, 100)
    sc.move_servo(pwm,8, 100)
    sc.move_servo(pwm,9, 270)
    
def check_dist():

##############3
    i=0
    avgDistance=0
    for i in range(5):
        GPIO.output(TRIG, False)                 #Set TRIG as LOW
        time.sleep(0.1)                                   #Delay

        GPIO.output(TRIG, True)                  #Set TRIG as HIGH
        time.sleep(0.00001)                           #Delay of 0.00001 seconds
        GPIO.output(TRIG, False)                 #Set TRIG as LOW

        while GPIO.input(ECHO)==0:              #Check whether the ECHO is LOW
        #     GPIO.output(led, False)             
            pulse_start = time.time()

        while GPIO.input(ECHO)==1:              #Check whether the ECHO is HIGH
        #     GPIO.output(led, False) 
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start #time to get back the pulse to sensor

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 (34300/2) to get distance
        distance = round(distance,2)                 #Round to two decimal points
        avgDistance=avgDistance+distance

    avgDistance=avgDistance/5
    print (avgDistance)
    # flag=0
    return avgDistance

    # if avgDistance < 15:      #Check whether the distance is within 15 cm range
    #     count=count+1
    #     home()

##########################################################################


if __name__ == "__main__":
    
    # print('Initialize PWM board controller')
    # Initialise the PCA9685 using the default address (0x40).
    pwm = Adafruit_PCA9685.PCA9685()

    print('Set frequency')
    # Set the frequency
    pwm.set_pwm_freq(sc.SERVO_MOTOR_FREQUENCY)
    time.sleep(2)
    home(pwm)
    while True:
        dist = check_dist()
        print(dist)
        if dist < 15:
            print("picking up")
            pickup(pwm)
            print("home")
            home(pwm)
