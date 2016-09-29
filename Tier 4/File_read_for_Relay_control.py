#!/usr/bin/python
import os
import RPi.GPIO as GPIO

class switch(object):
    value = None
    def __new__(class_,value ):
        class_.value = value
        return True
def case (*args):
    return any((arg==switch.value for arg in args ))

string = ''
prev_string = 'R00000000X'
flag = 0


relay_1  = ''
relay_2  = ''
relay_3  = ''
relay_4  = ''
relay_5  = ''
relay_6  = ''
relay_7  = ''
relay_8  = ''
error_state = ''

def gpio_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(28, GPIO.OUT)
    GPIO.setup(29, GPIO.OUT)
    GPIO.setup(30, GPIO.OUT)
    GPIO.setup(31, GPIO.OUT)
    GPIO.setup(4, GPIO.OUT)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)


    GPIO.output(28, False)
    GPIO.output(29, False)
    GPIO.output(30, False)
    GPIO.output(31, False)
    GPIO.output(4,False)
    GPIO.output(17, False)
    GPIO.output(18, False)
    GPIO.output(22, False)


def file_read():
    global string
    fo = open("/home/pi/gpio.txt", "r+")
    string = fo.read(10);
    fo.close()
   
def file_write_relay_state():
    global relay_1
    global relay_2
    global relay_3
    global relay_4
    global relay_5
    global relay_6
    global relay_7
    global relay_8
    global error_state

    fo = open("/home/pi/Relay.txt", "w")
    fo.write("Relay : 1 : " + relay_1 + "\n")
    fo.write("Relay : 2 : " + relay_2 + "\n")
    fo.write("Relay : 3 : " + relay_3 + "\n")
    fo.write("Relay : 4 : " + relay_4 + "\n")
    fo.write("Relay : 5 : " + relay_5 + "\n")
    fo.write("Relay : 6 : " + relay_6 + "\n")
    fo.write("Relay : 7 : " + relay_7 + "\n")
    fo.write("Relay : 8 : " + relay_8 + "\n")
    fo.write("Error : " + error_state + "\n")
    fo.close()

def string_check():
        global string
        global flag
        global prev_string
        global error_state
        string_length=len(string)
        
        if(string_length != 10 ):
                print ("Error: String not of required length") 
                error_state =  "String not of required length" 
                flag = 1
    
        if(string_length == 10):
            if string[0]!='R': 
                    print ("Error: Expected characters not found")  
                    error_state = "Expected characters not found"
                    flag = 1
            
    
            if string[9] != 'X':
                    print ("Error: Expected characters not found")
                    error_state = "Expected characters not found"
                    flag = 1
       
        #Check if any other digit other than 1 or 0 exists
            for i in range(1,9):
                if string[i] not in ('1','0'):
                    print ("Error: Expected characters not found")
                    error_state =  "Expected characters not found"
                    flag = 1
                
        if flag == 0:            
           prev_string = string
        
    
def relay_control():
    global string
    global flag
    global prev_string
    global relay_1
    global relay_2
    global relay_3
    global relay_4
    global relay_5
    global relay_6
    global relay_7
    global relay_8

    relay_num = []
    
    if flag == 0:   
        for i in range(1,10):
           if string[i].isdigit():
               relay_num.append(int(string[i]))
               
    elif flag == 1:
        for i in range(1,10):
           if prev_string [i].isdigit():
               relay_num.append(int(prev_string[i]))
        flag = 0

    for i in range(0,8):
        while switch(i):
                    if case(0):
                        if relay_num[i] == 1:
                            GPIO.output(28, True)
                            relay_1 = 'ON'
                            print ("Relay 1: ON")
                        else:
                            GPIO.output(28, False)
                            relay_1 = 'OFF'
                            print ("Relay 1: OFF")
                        break
                    if case(1):
                        if relay_num[i] == 1:
                            GPIO.output(29, True)
                            relay_2 = 'ON'
                            print ("Relay 2: ON")
                        else:
                            GPIO.output(29, False)
                            relay_2 = 'OFF'
                            print ("Relay 2: OFF")
                        break
                    if case(2):
                        if relay_num[i] == 1:
                            GPIO.output(30, True)
                            relay_3 = 'ON'
                            print ("Relay 3: ON")
                        else:
                            GPIO.output(30, False)
                            relay_3 = 'OFF'
                            print ("Relay 3: OFF")
                        break
                    if case(3):
                        if relay_num[i] == 1:
                            GPIO.output(31, True)
                            relay_4 = 'ON'
                            print ("Relay 4: ON")
                        else:
                            GPIO.output(31, False)
                            relay_4 = 'OFF'
                            print ("Relay 4: OFF")
                        break
                    if case(4):
                        if relay_num[i] == 1:
                            GPIO.output(4, True)
                            relay_5 = 'ON'
                            print ("Relay 5: ON")
                        else:
                            GPIO.output(4, False)
                            relay_5 = 'OFF'
                            print ("Relay 5: OFF")
                        break
                    if case(5):
                        if relay_num[i] == 1:
                            GPIO.output(17, True)
                            relay_6 = 'ON'
                            print ("Relay 6: ON")
                        else:
                            GPIO.output(17, False)
                            relay_6 = 'OFF'
                            print ("Relay 6: OFF")
                        break
                    if case(6):
                        if relay_num[i] == 1:
                            GPIO.output(18, True)
                            relay_7 = 'ON'
                            print ("Relay 7: ON")
                        else:
                            GPIO.output(18, False)
                            relay_7 = 'OFF'
                            print ("Relay 7: OFF")
                        break
                    if case(7):
                        if relay_num[i] == 1:
                            GPIO.output(22, True)
                            relay_8 = 'ON'
                            print ("Relay 8: ON")
                        else:
                            GPIO.output(22, False)
                            relay_8 = 'OFF'
                            print ("Relay 8: OFF")
                        break
    print ("-----------------------------------")
    file_write_relay_state()

try:
    gpio_setup()
    while 1 :
        file_read()
        string_check()
        relay_control()

except KeyboardInterrupt:
    print("Exited")
