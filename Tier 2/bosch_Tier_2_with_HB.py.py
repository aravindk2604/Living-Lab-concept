from init import *
from hear_beat_generate import *
# A semaphore to indicate that an item is available
available = threading.Semaphore(0)

# An event to indicate that processing is complete
completed = threading.Event()


humidity = ''
temp_C = ''
temp_F = ''
luminance = ''
gps_lat = ''
gps_long = ''
gps_time = ''

pir_1 = []
pir_2 = []
load_cell = []
door = []
smart_switch_1 = []
smart_switch_2 = []



last_p = ''
last_q = ''
last_c = ''
last_d = ''
last_s = ''
last_z = ''

file_num = 0

def sensitive_sensor(sensor_name):
    global pir_1
    global pir_2
    global door
    global smart_switch_1
    global smart_switch_2
    global last_p
    global last_q
    global last_d
    global last_z
    global last_s
    num = []
    S = []
    Z = []
    P = []
    Q = []
    D = []   

    while 1:
       ch = ser.read()
       if ch == 'x':
        break
       else:
        num.append(ch)

    while switch(sensor_name):
            if case('P'):                
                P = num
                break
            if case('Q'):               
                Q = num
                break
            if case('D'):               
                D = num
                break
            if case('S'): 
                S = num
                break
            if case('Z'):
                Z = num
                break
    num = []
    pir_1 = pir_1 + P
    pir_2 = pir_2 + Q
    door = door + D
    smart_switch_1 = smart_switch_1 + S
    smart_switch_2 = smart_switch_2 + Z

    last_s = S[len(S)-1]
    last_z = Z[len(Z)-1]
    last_d = D[len(D)-1]
    last_p = P[len(P)-1]
    last_q = Q[len(Q)-1]

def normal_sensor(sensor_name):
    global humidity
    global luminance
    num = ''
    while 1:
       ch = ser.read()
       if ch == 'x':
           break
       else:
            num = num + ch
    while switch(sensor_name):
        if case('H'):        
                humidity = num
                break
        if case('L'):                 
                luminance = num
                break
    num = ''


def sensor_gps():
    global gps_lat
    global gps_long
    global gps_time
    
    time_hrs = ''
    time_min = ''
    time_sec = ''
    lat_deg = ''
    lat_min = ''
    lat_sec = ''
    lat = ''
    long_deg = ''
    long_min = ''
    long_sec = ''
    long = ''
    
    
    ch = ser.read()
    while ch != ',':
        time_hrs = time_hrs + ch
        ch = ser.read()
        
    ch = ser.read()    
    while ch != ',':
        time_min = time_min + ch
        ch = ser.read()
        
    ch = ser.read()    
    while ch != '*':
        time_sec = time_sec + ch
        ch = ser.read()
        
    ch = ser.read()    
    while ch != ',':
        lat_deg = lat_deg + ch
        ch = ser.read()

    ch = ser.read()    
    while ch != ',':
        lat_min = lat_min + ch
        ch = ser.read()
    
    ch = ser.read()    
    while ch != ',':
        lat_sec = lat_sec + ch
        ch = ser.read()

    ch = ser.read()    
    while ch != '*':
        lat = lat + ch
        ch = ser.read()
    
    ch = ser.read()    
    while ch != ',':
        long_deg = long_deg + ch
        ch = ser.read()

    ch = ser.read()    
    while ch != ',':
        long_min = long_min + ch
        ch = ser.read()
   
    ch = ser.read()    
    while ch != ',':
        long_sec = long_sec + ch
        ch = ser.read()
    
    ch = ser.read()    
    while ch != 'x':
        long = long + ch
        ch = ser.read()    
   
    
    gps_lat = lat_deg + ' D ' + lat_min + '\' ' + lat_sec + '\'\' ' +lat
    gps_long = long_deg + ' D ' + long_min + '\' ' + long_sec + '\'\' ' + long 
    gps_time = time_hrs + ' H ' + time_min + ' M ' + time_sec + ' S ' 
    

def sensor_load_cell():
    global load_cell
    global last_c
    num = ''
    temp_L = []
    L = []
    while 1:
       ch = ser.read()
       if ch == 'x':
           temp_L.append(num)
           break
       elif ch == ',':
            temp_L.append(num)
            num = ''
       else:
            num = num + ch
    num=''
    L = L + temp_L
    load_cell = load_cell + L
    last_c = L[len(L)-1]


def sensor_temp():
    global temp_F
    global temp_C
    num = ''
    while 1:
       ch = ser.read()
       if ch == 'x':
           temp_F = num
           break
       elif ch == ',':
            temp_C = num
            num = ''
       else:
            num = num + ch
    num=''

def read_data(poll_num):  
    try:
        ser.write(poll_num)
        while 1 :              
                    ch = ser.read()
                    if ch == 'H' and humidity_state == True:
                        normal_sensor('H')
                        
                    elif ch =='L' and luminance_state == True:
                        normal_sensor('L')
                        
                    elif ch =='P' and pir_1_state == True:
                        sensitive_sensor('P')
                        
                    elif ch =='Q' and pir_2_state == True:
                        sensitive_sensor('Q')
                        
                    elif ch =='C' and load_cell_state == True:
                        sensor_load_cell()

                    elif ch =='D' and door_state == True:
                        sensitive_sensor('D')

                    elif ch =='S' and smart_swtich_1_state == True:
                        sensitive_sensor('S')

                    elif ch =='Z' and smart_swtich_2_state == True:
                        sensitive_sensor('Z')
                
                    elif ch =='T' and temp_state == True:
                        sensor_temp()

                    elif ch =='G' and gps_state == True:
                        sensor_gps()

                    elif ch == 'M':
                       return

                    

    except :
	pass
                   

@timeout(Sensor_poll_timeout_time_in_sec)
def read_msp1():
    read_data('1') 
    
@timeout(Sensor_poll_timeout_time_in_sec)
def read_msp2():
    read_data('2') 
            
@timeout(Sensor_poll_timeout_time_in_sec)   
def read_msp3():
    read_data('3')  


def polling():
    try:  
        read_msp1()
        read_msp2()
        read_msp3()
    except:
        pass


def log_before_xml():
    global humidity
    global temp_C
    global temp_F
    global luminance
    global gps_lat
    global gps_long
    global gps_time
    global smart_switch_1
    global smart_switch_2
    global pir_1
    global pir_2
    global load_cell
    global door
    logger.debug("Starting")
    logger.debug( "Humidity:" + humidity )
    logger.debug( "Luminance:" + luminance )
    logger.debug( "Temperature in C:" + temp_C )
    logger.debug( "Temperature in F:" + temp_F )
    logger.debug( "PIR 1:" + pir_1 )
    logger.debug( "PIR 2:" + pir_2 )
    logger.debug( "Door :" + door ) 
    logger.debug("Load Cell:" + load_cell)
    logger.debug( "Smart Switch 1:" + smart_switch_1 )
    logger.debug( "Smart Switch 2:" + smart_switch_2 )
    logger.debug( "Time: " + gps_time + "Latitude: " +  gps_lat + "Longitude: " + gps_long )


def log_after_xml():
    global humidity
    global temp_C
    global temp_F
    global luminance
    global gps_lat
    global gps_long
    global gps_time
    global smart_switch_1
    global smart_switch_2
    global pir_1
    global pir_2
    global load_cell
    global door
    logger1.debug("Starting")
    logger1.debug( "Humidity:" + humidity )
    logger1.debug( "Luminance:" + luminance )
    logger1.debug( "Temperature in C:" + temp_C )
    logger1.debug( "Temperature in F:" + temp_F )       
    logger1.debug( "PIR 1:" + pir_1 )
    logger1.debug( "PIR 2:" + pir_2 )
    logger1.debug( "Door :" + door )
    logger.debug("Load Cell:" + load_cell)
    logger1.debug( "Smart Switch 1:" + smart_switch_1 )
    logger1.debug( "Smart Switch 2:" + smart_switch_2 )
    logger1.debug( "Time: " + gps_time + "Latitude: " +  gps_lat + "Longitude: " + gps_long )


def generate_xml():
    global humidity
    global temp_C
    global temp_F
    global luminance
    global gps_lat
    global gps_long
    global gps_time
    global smart_switch_1
    global smart_switch_2
    global pir_1
    global pir_2
    global load_cell
    global door
	global file_num

    if log_status == True:
        log_before_xml()

	try:
            largest = max(len(smart_switch_1),len(smart_switch_2),len(pir_1),len(pir_2),len(door),len(load_cell),1)
            len_s = len(smart_switch_1)
            len_z = len(smart_switch_2)
            len_p = len(pir_1)
            len_q = len(pir_2)
            len_c = len(load_cell)
            len_d = len(door)

            i = 0
            for i in range(largest):
                print("Generating xml" + str(file_num ))
                sensors = Element('sensors')    
                tree=ElementTree(sensors)

                sensor1 = Element('sensor')
                sensors.append(sensor1)

                # FOR GPS
                if gps_xml == True and gps_lat !='' and gps_long !='' and gps_time != '': 
                    
                    sensor1.set('description','GPS')
                    sensor1.set('sensorName','GPS')
                    sensor_feature = SubElement(sensor1,'SensorFeatures')

                    sensor_details1 = SubElement(sensor_feature,'sensorDetails')
                    attributeName = Element('attributeName')
                    attributeVal = Element('attributeVal')
                    attributeName.text = 'LAT'
                    attributeVal.text = gps_lat
                    sensor_details1.append(attributeName)
                    sensor_details1.append(attributeVal)

                    sensor_details2 = SubElement(sensor_feature,'sensorDetails')
                    attributeName = Element('attributeName')
                    attributeVal = Element('attributeVal')
                    attributeName.text = 'LONG'
                    attributeVal.text = gps_long
                    sensor_details2.append(attributeName)
                    sensor_details2.append(attributeVal)

                    sensor_details3 = SubElement(sensor_feature,'sensorDetails')
                    attributeName = Element('attributeName')
                    attributeVal = Element('attributeVal')
                    attributeName.text = 'TIME'
                    attributeVal.text = gps_time
                    sensor_details3.append(attributeName)
                    sensor_details3.append(attributeVal)
                    

                # FOR LUMINANCE
                if luminance_xml == True and luminance !='':
                    
                    sensor2 = Element('sensor')
                    sensors.append(sensor2)

                    sensor2.set('description','LUMINANCE')
                    sensor2.set('sensorName','LUMINANCE')
                    sensor_feature = SubElement(sensor2,'SensorFeatures')

                    sensor_details1 = SubElement(sensor_feature,'sensorDetails')
                    attributeName = Element('attributeName')
                    attributeVal = Element('attributeVal')
                    attributeName.text = 'LIGHT'
                    attributeVal.text = luminance
                    sensor_details1.append(attributeName)
                    sensor_details1.append(attributeVal)
                
                
                # FOR LOADCELL
                if load_cell_xml == True and i < len_c:
                    
                    sensor3 = Element('sensor')
                    sensors.append(sensor3)

                    sensor3.set('description','LOADCELL')
                    sensor3.set('sensorName','LOADCELL')
                    sensor_feature = SubElement(sensor3,'SensorFeatures')

                    sensor_details1 = SubElement(sensor_feature,'sensorDetails')
                    attributeName = Element('attributeName')
                    attributeVal = Element('attributeVal')
                    attributeName.text = 'PRESSURE'
                    attributeVal.text = load_cell.pop(0)
                    sensor_details1.append(attributeName)
                    sensor_details1.append(attributeVal)
                    

                # FOR PIR SENSOR 1
                if pir_1_xml == True and i < len_p:
                    
                    sensor4 = Element('sensor')
                    sensors.append(sensor4)

                    sensor4.set('description','PIR#1')
                    sensor4.set('sensorName','PIR#1')
                    sensor_feature = SubElement(sensor4,'SensorFeatures')

                    sensor_details1 = SubElement(sensor_feature,'sensorDetails')
                    attributeName = Element('attributeName')
                    attributeVal = Element('attributeVal')
                    attributeName.text = 'MOTION'
                    attributeVal.text = pir_1.pop(0)
                    sensor_details1.append(attributeName)
                    sensor_details1.append(attributeVal)
                    
                
                # FOR PIR SENSOR 2
                if pir_2_xml == True and i < len_q:
                    
                    sensor5 = Element('sensor')
                    sensors.append(sensor5)

                    sensor5.set('description','PIR#2')
                    sensor5.set('sensorName','PIR#2')
                    sensor_feature = SubElement(sensor5,'SensorFeatures')

                    sensor_details1 = SubElement(sensor_feature,'sensorDetails')
                    attributeName = Element('attributeName')
                    attributeVal = Element('attributeVal')
                    attributeName.text = 'MOTION'
                    attributeVal.text = pir_2.pop(0)
                    sensor_details1.append(attributeName)
                    sensor_details1.append(attributeVal)
                    
               
                # FOR Temperature
                if temp_xml == True and temp_C != '' and temp_F !='':
                    
                    sensor6 = Element('sensor')
                    sensors.append(sensor6)

                    sensor6.set('description','TEMPERATURE')
                    sensor6.set('sensorName','TEMPERATURE')
                    sensor_feature = SubElement(sensor6,'SensorFeatures')

                    sensor_details1 = SubElement(sensor_feature,'sensorDetails')
                    attributeName = Element('attributeName')
                    attributeVal = Element('attributeVal')
                    attributeName.text = 'TEMPF'
                    attributeVal.text = temp_F
                    sensor_details1.append(attributeName)
                    sensor_details1.append(attributeVal)

                    sensor_details2 = SubElement(sensor_feature,'sensorDetails')
                    attributeName = Element('attributeName')
                    attributeVal = Element('attributeVal')
                    attributeName.text = 'TEMPC'
                    attributeVal.text = temp_C
                    sensor_details2.append(attributeName)
                    sensor_details2.append(attributeVal)
                    

                # FOR HUMIDITY
                if humidity_xml == True and humidity != '':
                    
                    sensor7 = Element('sensor')
                    sensors.append(sensor7)

                    sensor7.set('description','HUMIDITY')
                    sensor7.set('sensorName','HUMIDITY')
                    sensor_feature = SubElement(sensor7,'SensorFeatures')

                    sensor_details1 = SubElement(sensor_feature,'sensorDetails')
                    attributeName = Element('attributeName')
                    attributeVal = Element('attributeVal')
                    attributeName.text = 'HUMID'
                    attributeVal.text = humidity
                    sensor_details1.append(attributeName)
                    sensor_details1.append(attributeVal)
                    
                
                # FOR DOOR SENSOR
                if door_xml == True and i < len_d:
                    
                    sensor8 = Element('sensor')
                    sensors.append(sensor8)

                    sensor8.set('description','DOOR')
                    sensor8.set('sensorName','DOOR')
                    sensor_feature = SubElement(sensor8,'SensorFeatures')

                    sensor_details1 = SubElement(sensor_feature,'sensorDetails')
                    attributeName = Element('attributeName')
                    attributeVal = Element('attributeVal')
                    attributeName.text = 'STATE'
                    attributeVal.text = door.pop(0)
                    sensor_details1.append(attributeName)
                    sensor_details1.append(attributeVal)
                    

                # FOR SMART SWITCH 1
                if smart_swtich_1_xml == True and i < len_s:
                    
                    sensor9 = Element('sensor')
                    sensors.append(sensor9)

                    sensor9.set('description','SMARTSWITCH1')
                    sensor9.set('sensorName','SMARTSWITCH1')
                    sensor_feature = SubElement(sensor9,'SensorFeatures')

                    sensor_details1 = SubElement(sensor_feature,'sensorDetails')
                    attributeName = Element('attributeName')
                    attributeVal = Element('attributeVal')
                    attributeName.text = 'STATE'
                    attributeVal.text = smart_switch_1.pop(0)
                    sensor_details1.append(attributeName)
                    sensor_details1.append(attributeVal)
                    
                
                # FOR SMART SWITCH 2
                if smart_swtich_2_xml == True and i < len_z:
                    
                    sensor10 = Element('sensor')
                    sensors.append(sensor10)

                    sensor10.set('description','SMARTSWITCH2')
                    sensor10.set('sensorName','SMARTSWITCH2')
                    sensor_feature = SubElement(sensor10,'SensorFeatures')

                    sensor_details1 = SubElement(sensor_feature,'sensorDetails')
                    attributeName = Element('attributeName')
                    attributeVal = Element('attributeVal')
                    attributeName.text = 'STATE'
                    attributeVal.text = smart_switch_2.pop(0)
                    sensor_details1.append(attributeName)
                    sensor_details1.append(attributeVal)
                
                 
                if file_num > 9999999:
                    file_num = 0
                else:
                    file_num = file_num + 1


                xml_fname = 'sensors' + str(file_num) + '.xml' 

                tree.write(xml_fname)

                upload(xml_fname)

        except:
            pass
    
def upload(xml_fname):
    try:
        if log_status == True:
            log_after_xml()
        if os.path.getsize(xml_fname) > 100:
            cmd = "curl -X POST -F \"file=@"+xml_fname+"\" " + url_path
            os.system(cmd)     
        os.remove('/home/pi/' + str(xml_fname))
    except:
        pass

def heart_beat_upload():

    global humidity
    global temp_C
    global temp_F
    global luminance
    global gps_lat
    global gps_long
    global gps_time
    global last_p
    global last_q
    global last_d
    global last_z
    global last_s
    try:
        if log_status == True:
            log_after_xml()
        generate_xml_heat_beat(humidity,luminance, temp_C,temp_F,last_p, last_q ,last_d,last_s,last_z,gps_time,gps_lat,gps_long)
        cmd = "curl -X POST -F \"file=@hear_beat_upload.xml\" " + url_path
        os.system(cmd)     
        os.remove('/home/pi/hear_beat_upload.xml')
    except:
        pass
        
         
# A worker thread
def gen_up():
    while True:
        available.acquire()
	generate_xml()
        completed.set()
        

# A producer thread
def poll():
    while True:	
	completed.clear()       # Clear the event
	polling()
	t2 = threading.Thread(target=gen_up)
	t2.deamon = True
	t2.start()
	available.release()     # Signal on the semaphore
	completed.wait()
       


try:
	while True:

        if heart_beat_mode == True:
            t3 = threading.Thread(target=hear_beat_upload)
            t3.deamon = True
            t3.start()

		poll()

except:
	pass

