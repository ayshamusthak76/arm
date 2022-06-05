import serial
import time
arduino = serial.Serial(port='COM14', baudrate=115200, timeout=.1)
def write_read(x):
    # arduino.write(bytes(x, 'utf-8'))
    arduino.write(bytes(x,'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    # data = arduino.readline().decode("ascii")
    return data
servolist =[0]*6
while True:
    # num = input("Enter a number: ") # Taking input from user
    userInput = input("Get data points?")
    
    if userInput =='y':
    #     for i in range(6):
    #         data=write_read("0,1,2,3,4,5")
    #         servolist[i]=data
        data = write_read("1")

    print(type(data))
    # num = "0,1,2,3,4,5"
    # value = write_read(num)
    # print(servolist) # printing the value2
