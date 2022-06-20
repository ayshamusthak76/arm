import speech_recognition as sr
from datetime import date, datetime
from time import sleep
import pyttsx3


# Import blinka python modules.
import board
import digitalio


import Servo_control as sc

import time
import Adafruit_PCA9685
#here


r = sr.Recognizer()
mic = sr.Microphone()

print("hello")

# engine = pyttsx3.init('sapi5')
# # voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)

engine = pyttsx3.init("espeak")
engine.setProperty('rate', 178)
engine.setProperty('volume', 0.9)
voices = engine.getProperty('voices')
# print(voices)

# for voice in voices:
engine.setProperty('voice', voices[11].id)
#     print(voice.id)
#     # engine.say('The quick brown fox jumped over the lazy dog.')
#     engine.say("Hello, I am robot")
print('length',len(voices))

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
    speak("I am a rontos How may I help you?")
    print("Taking robot to home")
    # arm.home(pwm)

mic = sr.Microphone()
def takeCommand():
    query = None
    while query is None:
        r = sr.Recognizer()
        with mic as source:
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
            # speak("Say that again please...")
            query = None
        
    # if 'time' in words:
    if query.find('time') != -1:
        strTime = datetime.now().strftime("%H:%M:%S")
        speak(f"{MASTER} the time is {strTime}")
    
    # elif 'stop' in words:
    elif query.find('stop') != -1:

        speak("Getting the motors to a stop!")

    # elif 'start moving' or 'get going' in words:
    elif query.find('start') != -1:
        speak("Sure! Will get the robot started!")      
    
if __name__ == "__main__":
    print("Initializing Amity Bot")
    # speak("Initializing... Amity Bot...")

    pwm = Adafruit_PCA9685.PCA9685()

    print('Set frequency')
    pwm.set_pwm_freq(sc.SERVO_MOTOR_FREQUENCY)
    wishMe()
    while True:      
        takeCommand()
    
########################################


# import speech_recognition as sr
# from datetime import date, datetime
# from time import sleep
# import pyttsx3
# # import sonic_arm as sa
# import car 

# engine = pyttsx3.init("espeak")
# engine.setProperty('rate', 178)
# engine.setProperty('volume', 1.0)
# voices = engine.getProperty('voices')
# # print(voices)
# car_start=0
# # for voice in voices:
# engine.setProperty('voice', voices[11].id)

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# MASTER = ""

# def wishMe():
#     hour = int(datetime.now().hour)
    
#     if hour>=0 and hour<12:
#         speak("Good Morning!" + MASTER)
#     elif hour>=12 and hour<18:
#         speak("Good Afternoon!" + MASTER)
#     else:
#         speak("Good Evening!" + MASTER)
#     speak("I am RONTOS.. How may I help you?")
#     # sa.wave(pwm)
    

# def takeCommand():
#     global car_start
#     query = None
#     while query is None:
#         r = sr.Recognizer()
#         with sr.Microphone() as source:
#             print("Listening...")
#             # speak("Beep")
#             audio = r.listen(source)

#         try:
#             print("Recognising...")
#             query = r.recognize_google(audio, language= 'en-us')
#             # query = r.recognize_google(audio)
#             print(f"user said: {query}\n")
#             print(query)
#             words = query.split() #split the sentence into individual words         

#         except Exception:
#             print("Say that again please...")
#             # speak("Say that again please...")
#             query = None
        
#     # if 'time' in words:
#     if query.find('time') != -1:
#         strTime = datetime.now().strftime("%H:%M:%S")
#         speak(f"{MASTER} the time is {strTime}")
    
#     # elif 'stop' in words:
#     elif query.find('stop') != -1:
#         speak("Getting the motors to a stop!")
#         # car.stopcar(1)
#         car_start = 0
#         # if car_start == 0:
#         #     speak("Getting the motors to a stop!")
#         #     car.stopcar(1)
#         #     car_start = 0
#         # else:
#         #     speak("The car has not started yet! Let me know if you want to start it!")         
            

#     # elif 'start moving' or 'get going' in words:
#     elif query.find('start') != -1:
#         speak("Sure! Will get the robot started!") 
#         # car.start_car()  
#         car_start = 1
#         # if car_start != 0:
#         #     car_start = 1
#         #     speak("Sure! Will get the robot started!") 
#         #     car.start_car()
#         #     #car_Start function()
#         #     # 
#         # else:
#         #     speak("The car is already moving!")
    
#     return car_start




































    
# if __name__ == "__main__":
#     print("Initializing Amity Bot")
#     # speak("Initializing... Amity Bot...")
#     wishMe()
#     while True:      
#         takeCommand()


##########################

    # if 'timer' in query:
    #     speak("{MASTER} for how much time?")
    #     query2 = None
    #     while query2 is None:   
    #         r2 = sr.Recognizer()
    #         with sr.Microphone() as source:
    #             print("Listening...")
    #             speak("Beep")
    #             audio2 = r2.listen(source)

    #         try:
    #             print("Recognising...")
    #             query2 = r2.recognize_google(audio2, language= 'en-us')
    #             print(f"user said: {query2}\n")
    #             print(query2)
    #             break

    #         except Exception:
    #             print("Say that again please...")
    #             speak("Say that again please...")
    #             query2 = None
        
    #     time1 = ""

    #     for i in query2:
    #         if i.isdigit():
    #             time1 = time1 + i
    #     time2 = int(time1)

    #     if 'minutes'or 'minute' in query2:
    #         speak("Ok, your time starts now!")
    #         time.sleep(60*time2)
    #         speak("the time is up "+MASTER)

    #     elif 'seconds' in query2:
    #         speak("Ok, your time starts now!")
    #         time.sleep(time2)
    #         speak("the time is up "+MASTER)
            
    #     else:
    #         speak("No timer was set")

    # elif 'Google' in query:
    #     speak("{MASTER} what do you want to search")
    #     query2 = None
    #     while query2 is None:   
    #         r2 = sr.Recognizer()
    #         with sr.Microphone() as source:
    #             print("Listening...")
    #             speak("Beep")
    #             audio2 = r2.listen(source)

    #         try:
    #             print("Recognising...")
    #             query2 = r2.recognize_google(audio2, language= 'en-us')
    #             print(f"user said: {query2}\n")
    #             print(query2)
    #             break

    #         except Exception:
    #             print("Say that again please...")
    #             speak("Say that again please...")
    #             query2 = None

    #     query2 = query2.replace(" ","+")
    #     crome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    #     # webbrowser.get(crome_path).open(url = "https://www.google.com/search?sxsrf=ALeKk03LrBvejjuPt8DAQJem8SQiI9kzog%3A1584946711463&source=hp&ei=F154XsHBGfOf4-EP5rqiiAk&q="+query2+"&oq="+query2+"&gs_l=psy-ab.3..0i131j0j0i131l3j0j0i131j0l2j0i131.1780.2102..2729...2.0..0.181.356.0j2......0....1..gws-wiz.....10..35i362i39j35i39.ewj0sNfGivY&ved=0ahUKEwiBqePNgrDoAhXzzzgGHWadCJEQ4dUDCAY&uact=5") 


# while True:
#     with mic as source:
#         audio = r.listen(source)
#     words = r.recognize_google(audio)
#     print(words)

#     if  "today" in words:
#         print(date.today())
#         speak("The time is "+ date.today())


#     if "exit" in words:
#         print("...")
#         sleep(1)
#         print("Goodbye")
#         break


################################################################
# import pyttsx3
# import speech_recognition as sr
# import datetime
# # import wikipedia
# # import webbrowser
# import os
# import smtplib
# import time
# import serial

# port = "COM4"
# baudrate = 9600

# ArduinoSerial = serial.Serial(port, baudrate)
# time.sleep(2) #wait for 2 seconds for the communication to get established



# MASTER = "Parth Master..."

# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# def wishMe():
#     hour = int(datetime.datetime.now().hour)
    
#     if hour>=0 and hour<12:
#         speak("Good Morning" + MASTER)
#     elif hour>=12 and hour<18:
#         speak("Good Afternoon" + MASTER)
#     else:
#         speak("Good Evening" + MASTER)
#     speak("I am Jarvis... How may I help you?")

# def takeCommand():
#     query = None
#     while query is None:
#         r = sr.Recognizer()
#         with sr.Microphone() as source:
#             print("Listening...")
#             speak("Beep")
#             audio = r.listen(source)

#         try:
#             print("Recognising...")
#             query = r.recognize_google(audio, language= 'en-us')
#             print(f"user said: {query}\n")
#             print(query)

#         except Exception:
#             print("Say that again please...")
#             speak("Say that again please...")
#             query = None
    
#     # if 'Wikipedia' in query:
#     #     query = query.lower()
#     #     speak('Ok... I am searching in wikipedia')
#     #     query = query.replace("wikipedia","")
#     #     results = wikipedia.summary(query, sentences = 5 )
#     #     print(results)
#     #     speak(results)


#     # if 'YouTube' in query:
#     #     crome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
#     #     webbrowser.get(crome_path).open(url = "youtube.com")
    
#     if 'time' in query:
#         strTime = datetime.datetime.now().strftime("%H:%M:%S")
#         speak(f"{MASTER} the time is {strTime}")
    
#     if 'timer' in query:
#         speak("{MASTER} for how much time?")
#         query2 = None
#         while query2 is None:   
#             r2 = sr.Recognizer()
#             with sr.Microphone() as source:
#                 print("Listening...")
#                 speak("Beep")
#                 audio2 = r2.listen(source)

#             try:
#                 print("Recognising...")
#                 query2 = r2.recognize_google(audio2, language= 'en-us')
#                 print(f"user said: {query2}\n")
#                 print(query2)
#                 break

#             except Exception:
#                 print("Say that again please...")
#                 speak("Say that again please...")
#                 query2 = None
        
#         time1 = ""

#         for i in query2:
#             if i.isdigit():
#                 time1 = time1 + i
#         time2 = int(time1)

#         if 'minutes'or 'minute' in query2:
#             speak("Ok, your time starts now!")
#             time.sleep(60*time2)
#             speak("the time is up "+MASTER)

#         elif 'seconds' in query2:
#             speak("Ok, your time starts now!")
#             time.sleep(time2)
#             speak("the time is up "+MASTER)
            
#         else:
#             speak("No timer was set")

#     elif 'Google' in query:
#         speak("{MASTER} what do you want to search")
#         query2 = None
#         while query2 is None:   
#             r2 = sr.Recognizer()
#             with sr.Microphone() as source:
#                 print("Listening...")
#                 speak("Beep")
#                 audio2 = r2.listen(source)

#             try:
#                 print("Recognising...")
#                 query2 = r2.recognize_google(audio2, language= 'en-us')
#                 print(f"user said: {query2}\n")
#                 print(query2)
#                 break

#             except Exception:
#                 print("Say that again please...")
#                 speak("Say that again please...")
#                 query2 = None

#         query2 = query2.replace(" ","+")
#         crome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
#         # webbrowser.get(crome_path).open(url = "https://www.google.com/search?sxsrf=ALeKk03LrBvejjuPt8DAQJem8SQiI9kzog%3A1584946711463&source=hp&ei=F154XsHBGfOf4-EP5rqiiAk&q="+query2+"&oq="+query2+"&gs_l=psy-ab.3..0i131j0j0i131l3j0j0i131j0l2j0i131.1780.2102..2729...2.0..0.181.356.0j2......0....1..gws-wiz.....10..35i362i39j35i39.ewj0sNfGivY&ved=0ahUKEwiBqePNgrDoAhXzzzgGHWadCJEQ4dUDCAY&uact=5") 


# # def main():
# if __name__ == "__main__":
#     print("Initializing Jarvis")
#     speak("Initializing... Jarvis...")
#     while True:
         
#         # When u include arduino then uncomment below
#         # # incoming = str (ArduinoSerial.readline()) #read the serial data and print it as line
#         # if 'yes' in incoming:
#         wishMe()
#         takeCommand()
            
# # main()







##########################

    # if 'timer' in query:                                             
    #     speak("{MASTER} for how much time?")
    #     query2 = None
    #     while query2 is None:   
    #         r2 = sr.Recognizer()
    #         with sr.Microphone() as source:
    #             print("Listening...")
    #             speak("Beep")
    #             audio2 = r2.listen(source)

    #         try:
    #             print("Recognising...")
    #             query2 = r2.recognize_google(audio2, language= 'en-us')
    #             print(f"user said: {query2}\n")
    #             print(query2)
    #             break

    #         except Exception:
    #             print("Say that again please...")
    #             speak("Say that again please...")
    #             query2 = None
        
    #     time1 = ""

    #     for i in query2:
    #         if i.isdigit():
    #             time1 = time1 + i
    #     time2 = int(time1)

    #     if 'minutes'or 'minute' in query2:
    #         speak("Ok, your time starts now!")
    #         time.sleep(60*time2)
    #         speak("the time is up "+MASTER)

    #     elif 'seconds' in query2:
    #         speak("Ok, your time starts now!")
    #         time.sleep(time2)
    #         speak("the time is up "+MASTER)
            
    #     else:
    #         speak("No timer was set")

    # elif 'Google' in query:
    #     speak("{MASTER} what do you want to search")
    #     query2 = None
    #     while query2 is None:   
    #         r2 = sr.Recognizer()
    #         with sr.Microphone() as source:
    #             print("Listening...")
    #             speak("Beep")
    #             audio2 = r2.listen(source)

    #         try:
    #             print("Recognising...")
    #             query2 = r2.recognize_google(audio2, language= 'en-us')
    #             print(f"user said: {query2}\n")
    #             print(query2)
    #             break

    #         except Exception:
    #             print("Say that again please...")
    #             speak("Say that again please...")
    #             query2 = None

    #     query2 = query2.replace(" ","+")
    #     crome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    #     # webbrowser.get(crome_path).open(url = "https://www.google.com/search?sxsrf=ALeKk03LrBvejjuPt8DAQJem8SQiI9kzog%3A1584946711463&source=hp&ei=F154XsHBGfOf4-EP5rqiiAk&q="+query2+"&oq="+query2+"&gs_l=psy-ab.3..0i131j0j0i131l3j0j0i131j0l2j0i131.1780.2102..2729...2.0..0.181.356.0j2......0....1..gws-wiz.....10..35i362i39j35i39.ewj0sNfGivY&ved=0ahUKEwiBqePNgrDoAhXzzzgGHWadCJEQ4dUDCAY&uact=5") 


# while True:
#     with mic as source:
#         audio = r.listen(source)
#     words = r.recognize_google(audio)
#     print(words)

#     if  "today" in words:
#         print(date.today())
#         speak("The time is "+ date.today())


#     if "exit" in words:
#         print("...")
#         sleep(1)
#         print("Goodbye")
#         break


################################################################
# import pyttsx3
# import speech_recognition as sr
# import datetime
# # import wikipedia
# # import webbrowser
# import os
# import smtplib
# import time
# import serial

# port = "COM4"
# baudrate = 9600

# ArduinoSerial = serial.Serial(port, baudrate)
# time.sleep(2) #wait for 2 seconds for the communication to get established



# MASTER = "Parth Master..."

# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# def wishMe():
#     hour = int(datetime.datetime.now().hour)
    
#     if hour>=0 and hour<12:
#         speak("Good Morning" + MASTER)
#     elif hour>=12 and hour<18:
#         speak("Good Afternoon" + MASTER)
#     else:
#         speak("Good Evening" + MASTER)
#     speak("I am Jarvis... How may I help you?")

# def takeCommand():
#     query = None
#     while query is None:
#         r = sr.Recognizer()
#         with sr.Microphone() as source:
#             print("Listening...")
#             speak("Beep")
#             audio = r.listen(source)

#         try:
#             print("Recognising...")
#             query = r.recognize_google(audio, language= 'en-us')
#             print(f"user said: {query}\n")
#             print(query)

#         except Exception:
#             print("Say that again please...")
#             speak("Say that again please...")
#             query = None
    
#     # if 'Wikipedia' in query:
#     #     query = query.lower()
#     #     speak('Ok... I am searching in wikipedia')
#     #     query = query.replace("wikipedia","")
#     #     results = wikipedia.summary(query, sentences = 5 )
#     #     print(results)
#     #     speak(results)


#     # if 'YouTube' in query:
#     #     crome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
#     #     webbrowser.get(crome_path).open(url = "youtube.com")
    
#     if 'time' in query:
#         strTime = datetime.datetime.now().strftime("%H:%M:%S")
#         speak(f"{MASTER} the time is {strTime}")
    
#     if 'timer' in query:
#         speak("{MASTER} for how much time?")
#         query2 = None
#         while query2 is None:   
#             r2 = sr.Recognizer()
#             with sr.Microphone() as source:
#                 print("Listening...")
#                 speak("Beep")
#                 audio2 = r2.listen(source)

#             try:
#                 print("Recognising...")
#                 query2 = r2.recognize_google(audio2, language= 'en-us')
#                 print(f"user said: {query2}\n")
#                 print(query2)
#                 break

#             except Exception:
#                 print("Say that again please...")
#                 speak("Say that again please...")
#                 query2 = None
        
#         time1 = ""

#         for i in query2:
#             if i.isdigit():
#                 time1 = time1 + i
#         time2 = int(time1)

#         if 'minutes'or 'minute' in query2:
#             speak("Ok, your time starts now!")
#             time.sleep(60*time2)
#             speak("the time is up "+MASTER)

#         elif 'seconds' in query2:
#             speak("Ok, your time starts now!")
#             time.sleep(time2)
#             speak("the time is up "+MASTER)
            
#         else:
#             speak("No timer was set")

#     elif 'Google' in query:
#         speak("{MASTER} what do you want to search")
#         query2 = None
#         while query2 is None:   
#             r2 = sr.Recognizer()
#             with sr.Microphone() as source:
#                 print("Listening...")
#                 speak("Beep")
#                 audio2 = r2.listen(source)

#             try:
#                 print("Recognising...")
#                 query2 = r2.recognize_google(audio2, language= 'en-us')
#                 print(f"user said: {query2}\n")
#                 print(query2)
#                 break

#             except Exception:
#                 print("Say that again please...")
#                 speak("Say that again please...")
#                 query2 = None

#         query2 = query2.replace(" ","+")
#         crome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
#         # webbrowser.get(crome_path).open(url = "https://www.google.com/search?sxsrf=ALeKk03LrBvejjuPt8DAQJem8SQiI9kzog%3A1584946711463&source=hp&ei=F154XsHBGfOf4-EP5rqiiAk&q="+query2+"&oq="+query2+"&gs_l=psy-ab.3..0i131j0j0i131l3j0j0i131j0l2j0i131.1780.2102..2729...2.0..0.181.356.0j2......0....1..gws-wiz.....10..35i362i39j35i39.ewj0sNfGivY&ved=0ahUKEwiBqePNgrDoAhXzzzgGHWadCJEQ4dUDCAY&uact=5") 


# # def main():
# if __name__ == "__main__":
#     print("Initializing Jarvis")
#     speak("Initializing... Jarvis...")
#     while True:
         
#         # When u include arduino then uncomment below
#         # # incoming = str (ArduinoSerial.readline()) #read the serial data and print it as line
#         # if 'yes' in incoming:
#         wishMe()
#         takeCommand()
            
# # main()