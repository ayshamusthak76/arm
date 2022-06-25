import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
import time

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
	GPIO.output(Motor1A,GPIO.LOW)
	GPIO.output(Motor1B,GPIO.LOW)
	GPIO.output(Motor2A,GPIO.HIGH)
	GPIO.output(Motor2B,GPIO.HIGH)
	

def turnRight():
	print("Going Right")
	# GPIO.output(Motor1A,GPIO.LOW)
	# GPIO.output(Motor1B,GPIO.HIGH)
	# GPIO.output(Motor2A,GPIO.HIGH)
	# GPIO.output(Motor2B,GPIO.LOW)
	GPIO.output(Motor1A,GPIO.HIGH)
	GPIO.output(Motor1B,GPIO.HIGH)
	GPIO.output(Motor2A,GPIO.LOW)
	GPIO.output(Motor2B,GPIO.LOW)
	

def stop():
	print("Stopping")
	GPIO.output(Motor1A,GPIO.LOW)
	GPIO.output(Motor1B,GPIO.LOW)
	GPIO.output(Motor2A,GPIO.LOW)
	GPIO.output(Motor2B,GPIO.LOW)
