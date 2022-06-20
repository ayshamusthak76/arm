
import Adafruit_PCA9685
import Servo_control as sc
import sonic_arm as sa
import car
import speech as sp
import os



if __name__ == "__main__":
    pwm = Adafruit_PCA9685.PCA9685()

    print('Set frequency')
    pwm.set_pwm_freq(sc.SERVO_MOTOR_FREQUENCY)

    #Self Intro with a Wave
    # sp.wishMe()
    # sa.wave(pwm)


    # car_start = 0
    # while True:      

        # car_start=1
        # if car_start == 1:
        #     car.start_car()


        # execfile('car.py')
        os.system('python car.py')
        # subprocess.call()


        #Take command from user
        # car_start = sp.takeCommand()
        # if car_start == 1:
        #     car.start_car()
        # else:
        #     car.stopcar(1)
        # #Ultrasonic sensor reading
        # dist = sa.check_dist()
        # print(dist)
        # if dist < 26:
        #         sa.pickup(pwm,sa.dist)
        #         sa.dropoff(pwm)
        #         sa.home(pwm)



    