from init import *
from config_file import *

def generate_xml_heart_beat(humidity = '',luminance = '', temp_C = '',temp_F = '',pir_1 = '', pir_2 = '',door = '',smart_switch_1='',smart_switch_2='',gps_time='',gps_lat='',gps_long=''):
	try:

                print("Generating xml" + str(file_num ))
                sensors = Element('sensors')    
                tree=ElementTree(sensors)

                sensor1 = Element('sensor')
                sensors.append(sensor1)

                # FOR GPS
                if gps_xml == True:
                    
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
                if luminance_xml == True:
                    
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
                if load_cell_xml == True:
                    
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
                if pir_1_xml == True:
                    
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
                if pir_2_xml == True:
                    
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
                if temp_xml == True:
                    
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
                if humidity_xml == True:
                    
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
                if door_xml == True:
                    
                    sensor8 = Element('sensor')
                    sensors.append(sensor8)

                    sensor8.set('description','DOOR')
                    sensor8.set('sensorName','DOOR')
                    sensor_feature = SubElement(sensor8,'SensorFeatures')

                    sensor_details1 = SubElement(sensor_feature,'sensorDetails')
                    attributeName = Element('attributeName')
                    attributeVal = Element('attributeVal')
                    attributeName.text = 'STATE'
                    attributeVal.text = door
                    sensor_details1.append(attributeName)
                    sensor_details1.append(attributeVal)
                    

                # FOR SMART SWITCH 1
                if smart_swtich_1_xml == True:
                    
                    sensor9 = Element('sensor')
                    sensors.append(sensor9)

                    sensor9.set('description','SMARTSWITCH1')
                    sensor9.set('sensorName','SMARTSWITCH1')
                    sensor_feature = SubElement(sensor9,'SensorFeatures')

                    sensor_details1 = SubElement(sensor_feature,'sensorDetails')
                    attributeName = Element('attributeName')
                    attributeVal = Element('attributeVal')
                    attributeName.text = 'STATE'
                    attributeVal.text = smart_switch_1
                    sensor_details1.append(attributeName)
                    sensor_details1.append(attributeVal)
                    
                
                # FOR SMART SWITCH 2
                if smart_swtich_2_xml == True:
                    
                    sensor10 = Element('sensor')
                    sensors.append(sensor10)

                    sensor10.set('description','SMARTSWITCH2')
                    sensor10.set('sensorName','SMARTSWITCH2')
                    sensor_feature = SubElement(sensor10,'SensorFeatures')

                    sensor_details1 = SubElement(sensor_feature,'sensorDetails')
                    attributeName = Element('attributeName')
                    attributeVal = Element('attributeVal')
                    attributeName.text = 'STATE'
                    attributeVal.text = smart_switch_2
                    sensor_details1.append(attributeName)
                    sensor_details1.append(attributeVal)

                xml_fname = 'hear_beat_upload.xml'

                tree.write(xml_fname)
    except :
    	pass