import sr_new as sp
import cv2 as cv2
import RPi.GPIO as GPIO
import sr_car as car
import time
if __name__ == "__main__":
    print("Initializing Amity Bot")
    # speak("Initializing... Amity Bot...")
    sp.wishMe()
    # arm.wave()
    # arm.home()
    while True:      
        start_car=sp.takeCommand()
        if start_car:
            car.start_car()
        else:
            car.stop_car()