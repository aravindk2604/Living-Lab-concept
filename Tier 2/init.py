import serial
import os
import sys
import thread
import signal
import time
import logging
from timeout import timeout
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element,Comment,SubElement
import xml.etree.ElementTree as etree
import xml.dom.minidom
from config_file import *
from K_Thread import *


class switch(object):
    value = None
    def __new__(class_,value ):
        class_.value = value
        return True
def case (*args):
    return any((arg==switch.value for arg in args ))


logger = logging.getLogger('log_before_xml')
hdlr = logging.FileHandler('log_before_xml.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)


logger1 = logging.getLogger('log_after_xml')
hdlr1 = logging.FileHandler('log_after_xml.log')
formatter1 = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr1.setFormatter(formatter1)
logger1.addHandler(hdlr1) 
logger1.setLevel(logging.DEBUG)


logger3 = logging.getLogger('raw_data')
hdlr3 = logging.FileHandler('raw_data.log')
formatter3 = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr3.setFormatter(formatter3)
logger3.addHandler(hdlr3) 
logger3.setLevel(logging.DEBUG)

try:           
    ser = serial.Serial(port='/dev/ttyAMA0',baudrate='9600')
except:
    print "Serial port error"