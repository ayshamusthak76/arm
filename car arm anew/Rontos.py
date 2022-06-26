
import sonic_arm as sa
import speech as sp
import os

if __name__ == "__main__":

    #--------  Self Intro with a Wave -------   Working
    # sp.wishMe()
    # sa.wave(pwm)

    #-------- Take command from user  --------
    sp.takeCommand()

    # #Ultrasonic sensor reading and Car
    os.system('python car.py')


    # while True:

    #     dist = sa.check_dist()
        # os.system('python car.py')

        # if dist < 26:
        #     stopcar()                                                                                          
        #     sa.pickup(pwm,sa.dist)
        #     sa.dropoff(pwm)
        #     sa.home(pwm)
        #     continue




    