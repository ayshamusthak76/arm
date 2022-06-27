from flask import Flask, render_template, request, redirect, url_for, make_response
import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
import motors
import arm
import socket
import speech
import os
motors.stop()

# Get server ip
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
server_ip = s.getsockname()[0]
s.close()

app = Flask(__name__) 

@app.route('/')
def index():

	return render_template('index copy.html', server_ip=server_ip)

@app.route('/<changepin>', methods=['POST'])
def reroute(changepin):

	changePin = int(changepin) 

	if changePin == 1:
		motors.turnLeft()
	elif changePin == 2:
		motors.forward()
	elif changePin == 3:
		motors.turnRight()
	elif changePin == 4:
		motors.backward()
	elif changePin == 5:
		motors.stop()

	elif changePin == 6:	
		# arm.home()
	elif changePin == 7:
		arm.wave()
	elif changePin == 9:
		arm.pickup() 


	elif changePin == 8:
		speech.wishMe()
		while True:
			speech.takeCommand()         
			if speech.stoptalk:
				break
	      
	
	elif changePin == 10:
		os.system('python car.py')
	
	
	response = make_response(redirect(url_for('index')))
	return(response)

app.run(debug=True, host='0.0.0.0', port=8000) 