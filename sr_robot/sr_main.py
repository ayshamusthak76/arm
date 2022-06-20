import sr 
import sr_arm as arm
import cv2 as cv2
import RPi.GPIO as GPIO
import sr_car as car
import time
if __name__ == "__main__":
    print("Initializing Amity Bot")
    # speak("Initializing... Amity Bot...")
    sr.wishMe()
    arm.wave()
    arm.home()
    while True:      
        start_car,arm_pos=sr.takeCommand()
        if start_car:
            car.start_car()
        else:
            car.stop_car()