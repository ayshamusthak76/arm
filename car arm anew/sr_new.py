import speech_recognition as sr
from datetime import date, datetime
from time import sleep
import pyttsx3
import sr_arm as arm
# import sr_car as car
import os
import board
import digitalio

r = sr.Recognizer()
mic = sr.Microphone()

car_start = 0
arm_state = "home"

print("hello")

engine = pyttsx3.init("espeak")
engine.setProperty('rate', 178)
engine.setProperty('volume', 0.9)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[11].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

MASTER = ""

def wishMe():
    hour = int(datetime.now().hour)    
    if hour>=0 and hour<12:
        speak("Good Morning!" + MASTER)
    elif hour>=12 and hour<18:
        speak("Good Afternoon!" + MASTER)
    else:
        speak("Good Evening!" + MASTER)
    # speak("I am Rontos.. How may I help you?")
    speak("Mera naam Rontos hai. Mein aapko kaise madad kar sakta hoon")
    

def takeCommand():
    global car_start
    query = None
    while query is None:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            # speak("Beep")
            audio = r.listen(source)

        try:
            print("Recognising...")
            query = r.recognize_google(audio, language= 'en-us')
            # query = r.recognize_google(audio)
            print(f"user said: {query}\n")
            print(query)
            words = query.split() #split the sentence into individual words         

        except Exception:
            print("Say that again please...")
            query = None
        
    # if 'time' in words:
    if query.find('time') != -1:
        strTime = datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")
    
    # elif 'stop' in words:
    elif query.find('stop') != -1 or query.find('top') != -1:
        if car_start:
            car_start = 0
            speak("Getting the motors to a stop!")
            # car.stop_car()
        else:
            speak("The car has not started yet! Let me know if you want to start it!")                     

    # elif 'start moving' or 'get going' in words:
    elif query.find('start') != -1 or query.find('go') != -1:
        if car_start == 0:
            car_start = 1
            
            speak("Sure! Will get the robot started!") 
            os.system('python car.py')
            # car.start_car()
        else:
            speak("The car is already moving!")
    
    elif query.find('pick') != -1:
        car_start=0
        arm_state = "pickup"
        # car.stop_car()
        # arm.pickup()

    # return car_start
    
if __name__ == "__main__":
    print("Initializing Rontos")
    # speak("Initializing... Rontos...")
    wishMe()
    while True:      
        takeCommand()