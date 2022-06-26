import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
import time
# import Servo_control as sc
# import Adafruit_PCA9685

Motor1A = 20 
Motor1B = 27
Motor2A = 16
Motor2B = 22

# in1=20
# in2 = 16
# in3 = 27
# in4 = 22
en1 = 19
en2 = 26


# GPIO.setup(Motor1A,GPIO.OUT)
# GPIO.setup(Motor1B,GPIO.OUT)
# GPIO.setup(Motor2A,GPIO.OUT)
# GPIO.setup(Motor2B,GPIO.OUT)

# GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(en1, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
p1 = GPIO.PWM(en1, 100)
p2 = GPIO.PWM(en2, 100)
p1.start(80)
p2.start(80)
GPIO.output(Motor1A, GPIO.LOW)
GPIO.output(Motor1B, GPIO.LOW)
GPIO.output(Motor2A, GPIO.LOW)
GPIO.output(Motor2B, GPIO.LOW)

# pwm = Adafruit_PCA9685.PCA9685()

# print('Set frequency')
# # Set the frequency
# pwm.set_pwm_freq(sc.SERVO_MOTOR_FREQUENCY)

# p1 = GPIO.PWM(en1, 100)
# p2 = GPIO.PWM(en2, 100)
# p1.start(40)
# p2.start(40)

def backward():
	# GPIO.output(Motor1A,GPIO.HIGH)
	# GPIO.output(Motor1B,GPIO.LOW)
	# GPIO.output(Motor2A,GPIO.HIGH)
	# GPIO.output(Motor2B,GPIO.LOW)
	GPIO.output(Motor1A,GPIO.HIGH)
	GPIO.output(Motor1B,GPIO.LOW)
	GPIO.output(Motor2A,GPIO.LOW)
	GPIO.output(Motor2B,GPIO.HIGH)
	

def forward():
	# GPIO.output(Motor1A,GPIO.LOW)
	# GPIO.output(Motor1B,GPIO.HIGH)
	# GPIO.output(Motor2A,GPIO.LOW)
	# GPIO.output(Motor2B,GPIO.HIGH)
	GPIO.output(Motor1A,GPIO.LOW)
	GPIO.output(Motor1B,GPIO.HIGH)
	GPIO.output(Motor2A,GPIO.HIGH)
	GPIO.output(Motor2B,GPIO.LOW)

	
def turnLeft():
	print("Going Left")
	# GPIO.output(Motor1A,GPIO.HIGH)
	# GPIO.output(Motor1B,GPIO.LOW)
	# GPIO.output(Motor2A,GPIO.LOW)
	# GPIO.output(Motor2B,GPIO.HIGH)
	GPIO.output(Motor1A,GPIO.HIGH)
	GPIO.output(Motor1B,GPIO.HIGH)
	GPIO.output(Motor2A,GPIO.LOW)
	GPIO.output(Motor2B,GPIO.LOW)

def turnRight():
	print("Going Right")
	# GPIO.output(Motor1A,GPIO.LOW)
	# GPIO.output(Motor1B,GPIO.HIGH)
	# GPIO.output(Motor2A,GPIO.HIGH)
	# GPIO.output(Motor2B,GPIO.LOW)
	
	GPIO.output(Motor1A,GPIO.LOW)
	GPIO.output(Motor1B,GPIO.LOW)
	GPIO.output(Motor2A,GPIO.HIGH)
	GPIO.output(Motor2B,GPIO.HIGH)

# def home():
#     print('home')
#     sc.move_servo(pwm, 4, 135)
#     sc.move_servo(pwm,5, 160)
#     sc.move_servo(pwm, 6, 200)
#     sc.move_servo(pwm,7, 100)
#     sc.move_servo(pwm,8, 80)
#     sc.move_servo(pwm,9, 45)


# def wave():
#     print('wave')
#     sc.move_servo(pwm, 4, 135)
#     sc.move_servo(pwm, 5, 175) #find the values here
#     sc.move_servo(pwm, 6, 230)
    
#     sc.move_servo(pwm, 7, 200)
#     sc.move_servo(pwm, 8, 40)
#     sc.move_servo(pwm, 8, 140)
#     sc.move_servo(pwm, 4, 200)
#     sc.move_servo(pwm, 8, 40)
#     sc.move_servo(pwm, 8, 140)
	

def stop():
	print("Stopping")
	GPIO.output(Motor1A,GPIO.LOW)
	GPIO.output(Motor1B,GPIO.LOW)
	GPIO.output(Motor2A,GPIO.LOW)
	GPIO.output(Motor2B,GPIO.LOW)
