Enable = True
Disable = False

# Enbabling and Disabling Sensors

humidity_state = Enable
temp_state = Enable
luminance_state = Enable
pir_1_state = Enable
pir_2_state = Enable
load_cell_state = Enable
door_state = Enable
gps_state = Enable
smart_swtich_1_state = Enable
smart_swtich_2_state = Enable

# Web Server address to upload XML file
url_path = "http://192.168.1.12:8080/UPA/rest/sensors/putSensorDetails"

# Time out period for polling sensors
Sensor_poll_timeout_time_in_sec = 0.3   # .3 sec = 300 milli seconds

# Mode ---> 1 = Heart Beat or Time out ---- 2 = Sensor Specific 
mode = 1

# mode 1 --> Heart beat period for upload
Heart_beat_timout_period = 1 # 1 sec

#mode 2 --> Sensor Specific period for upload 
Sensor_specific_timeout_period = 0 # 0 sec

#Senor specific XML generation 'Enable' or 'Disable'
humidity_xml = Enable
temp_xml = Enable
luminance_xml = Enable
pir_1_xml = Enable
pir_2_xml = Enable
load_cell_xml = Enable
door_xml = Enable
gps_xml = Enable
smart_swtich_1_xml = Enable
smart_swtich_2_xml = Enable

#Print messages 'Enable' or 'Disable'
print_msg = Enable

# logging 'Enable' or 'Disable'
log_status = True

# Do not change
if mode == 1:
    upload_timeout = Heart_beat_timout_period
elif mode == 2:
    upload_timeout = Sensor_specific_timeout_period
