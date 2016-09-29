# Remote Relay (Server) Control
# Auther - Vimal (RBEI)

# Curl commands to test

# to check the server
	# curl -H "content-type: application/json" - X GET http://IP:PORT/
# to get relay value 
	# curl -H "content-type: application/json" - X GET http://IP:PORT/relay/2/OFF
# to set relay value 
	# curl -H "content-type: application/json" - X PUT http://IP:PORT/relay/1/ON


from flask import Flask, url_for, request , g, render_template, Response
from flask import json, jsonify
import sys

import os
import RPi.GPIO as GPIO


app = Flask(__name__)

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
    return

def string_check():
        global string
        global flag
        global prev_string
        global error_state
        string_length=len(string)
        
        if(string_length != 10 ):
                error_state =  "String not of required length" 
                flag = 1
    
        if(string_length == 10):
            if string[0]!='R':   
                    error_state = "Expected characters not found"
                    flag = 1
            
    
            if string[9] != 'X':
                    error_state = "Expected characters not found"
                    flag = 1
       
        #Check if any other digit other than 1 or 0 exists
            for i in range(1,9):
                if string[i] not in ('1','0'):
                    error_state =  "Expected characters not found"
                    flag = 1
                
        if flag == 0:            
           prev_string = string

        relay_control()
        
    
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
                        else:
                            GPIO.output(28, False)
                            relay_1 = 'OFF'
                        break
                    if case(1):
                        if relay_num[i] == 1:
                            GPIO.output(29, True)
                            relay_2 = 'ON'
                        else:
                            GPIO.output(29, False)
                            relay_2 = 'OFF'
                        break
                    if case(2):
                        if relay_num[i] == 1:
                            GPIO.output(30, True)
                            relay_3 = 'ON'
                        else:
                            GPIO.output(30, False)
                            relay_3 = 'OFF'
                        break
                    if case(3):
                        if relay_num[i] == 1:
                            GPIO.output(31, True)
                            relay_4 = 'ON'
                        else:
                            GPIO.output(31, False)
                            relay_4 = 'OFF'
                        break
                    if case(4):
                        if relay_num[i] == 1:
                            GPIO.output(4, True)
                            relay_5 = 'ON'
                        else:
                            GPIO.output(4, False)
                            relay_5 = 'OFF'
                        break
                    if case(5):
                        if relay_num[i] == 1:
                            GPIO.output(17, True)
                            relay_6 = 'ON'
                        else:
                            GPIO.output(17, False)
                            relay_6 = 'OFF'
                        break
                    if case(6):
                        if relay_num[i] == 1:
                            GPIO.output(18, True)
                            relay_7 = 'ON'
                        else:
                            GPIO.output(18, False)
                            relay_7 = 'OFF'
                        break
                    if case(7):
                        if relay_num[i] == 1:
                            GPIO.output(22, True)
                            relay_8 = 'ON'
                        else:
                            GPIO.output(22, False)
                            relay_8 = 'OFF'
                        break

def set_relay(value):
	print("Called")
	global string
	string = value
	string_check()

################################# Routes Decorators ###########################
# Root page
@app.route('/')
def api_root():
    return 'Welcome to Remote Relay Control. to update, POST IP:PORT/relay/<relay_id>/<ON/OFF>, to get: IP:PORT/relay/<relay_id>/'

### Control Relay (ON/OFF)  ###

@app.route('/<value>', methods = ['PUT'])
def api_feed(value):
	data = " Value = "+value + " method = "+request.method
	print data
	if request.method == 'PUT':
		if request.headers['Content-Type'] == 'text/plain':
		    set_relay(value)	
		    return data
		elif request.headers['Content-Type'] == 'application/json':			
		    set_relay(value)	
		    return "200" + data
		else:
		    return "415 Unsupported Media Type"




### Get the relay status
@app.route('/relay/<relay_id>', methods = ['GET'])
def api_get_relay(relay_id):
	value = "ON" # take the value from the actual relay control
	print "Get sensor data from "+relay_id
	data = {
		'relay'  : relay_id,
		'Value' : value  
	}
    	print data
    	return jsonify(data);

@app.route('/getrelay', methods = ['GET'])
def api_get_relay():
	global relay_1
    	global relay_2
    	global relay_3
    	global relay_4
    	global relay_5
    	global relay_6
    	global relay_7
    	global relay_8
	global error_state
	print "Get sensor data from all relay "
	data = {
		'relay1'  : relay_1,
		'relay2'  : relay_2,
		'relay3'  : relay_3,
		'relay4'  : relay_4,
		'relay5'  : relay_5,
		'relay6'  : relay_6,
		'relay7'  : relay_7,
		'relay8'  : relay_8,
		'Status'   : error_state
	}
    	print data
    	return jsonify(data);

###########################   Main #################################################
if __name__ == '__main__':
        gpio_setup()
	app.debug = True
	app.run(host='0.0.0.0')



