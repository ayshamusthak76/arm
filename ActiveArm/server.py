from flask import Flask, request , jsonify
import RPi.GPIO as GPIO
import ServoControl as sc

import time
import Adafruit_PCA9685


# base =  sc.move_servo(pwm,4,120)
# shoulder = 
# elbow = 
# pivot =
# wrist = 
# claw = 

# Mapping appliances/modules to words identifying them (in commands)
words = {"position" : {"home", "pickup"}
        #  "tube" : {"light", "tube", "tubelight"},
        #  "bulb" : {"bulb", "dim"}
        }

# Mapping appliances/modules to their ports 
# (220V Appliance --> Relay --> GPIO port) or (5V module/LED --> GPIO port)
# GPIO_ports = {"tube":31,
#               "cfan":33,
#               "bulb":37}

def homestate(pwm):
    sc.move_servo(pwm,4,120)
    time.sleep(3)
    sc.move_servo(pwm,5,120)
    time.sleep(3)
    sc.move_servo(pwm,6,120)
    time.sleep(3)
    sc.move_servo(pwm,7,120)
    time.sleep(3)
    sc.move_servo(pwm,8,120)
    time.sleep(3)
    sc.move_servo(pwm,9,120)
    time.sleep(3)

# GPIO.setmode(GPIO.BOARD) 

# def init_switches(inds):
#     """Initializes the ports as GPIO output ports. Initially Off.
#     inds    : list, Port numbers. 
#     """
#     for i in inds:
#         GPIO.setup(i, GPIO.OUT, initial = 0)

def checkpos(status):
    """Turns a port ON/True or OFF/False
    ind     : int, Port number
    status  : str, Turns port ON if status is 'on'. Else turns port OFF.
    """
    print("Taking arm to home position >>",status==1)
    # GPIO.output(ind, status=='on') #check later

def trigger(command_string):
    """Uses token-matching to act on a command.
    command_string  : str, Command. For example : "fan off", "turn the light on", etc.
    status          : str (optional), Turns port ON if status is 'on'. Else turns port OFF.
    """
    # Convert command to lower case and split into words
    command_words = set(command_string.lower().split(" "))
    # Set status to 'on' if the word 'on' is present in the command (command_words)
    status = 1 if 'home' in command_words else 0

    # Iterate over all appliances (ie. keys in words)
    for pos in words:
        # If the command contains any words referring to the appliance
        if command_words.intersection(words[pos]):
            # Trigger the appliance to status
            homestate(pwm)
            checkpos(status)
            return

app = Flask(__name__)

@app.route('/arm', methods=['POST'])
def prime():
    """Endpoint to process incoming requests. 
    (POST requests with JSON mapping 'obj' to command)"""
    cont = request.get_json()
    print("here")
    if cont is not None:
        trigger(command_string=cont['obj'])
    return jsonify({"SUCCESS":True})

if __name__ == '__main__':  
    print('Initialize PWM board controller')
    pwm = Adafruit_PCA9685.PCA9685()

    print('Set frequency')
    pwm.set_pwm_freq(sc.SERVO_MOTOR_FREQUENCY)
    
    print('Starting Server')
    # init_switches(GPIO_ports.values())
    print("hello")
    app.run(debug=True,
            use_reloader=False,
            host='0.0.0.0',
            port=8000
            ) #run app in debug mode on port 5000
