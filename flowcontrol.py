"""
@name: flowcontrol.py                      
@description:                  
    Module with main Arduino class for interacting with Arduino board

@author: Christopher Brittin   
@email: "cabrittin"+ <at>+ "gmail"+ "."+ "com"
@date: 2022-09
"""

from configparser import ConfigParser,ExtendedInterpolation
import serial
import time

### ARDUINO PINS ###
PIN_OFF = 0
PIN_INJECT = 1
PIN_FLUSH = 2
PIN_STIMULUS = 4 

### FIRMWARE CASES ###
SET_STATE = 1
SET_NUM_PATTERNS = 6 
SET_PATTERN = 5
SET_TIME_INTERVALS = 10
SET_PATTERN_REPEATS = 11
TRIGGER_PATTERNS = 12


class Arduino:
    def __init__(self,firmwareVersion='MM-Ard-2',port='/dev/ttyACM0',baudrate=57600,timeout=1,config_file=None):
        if config_file is not None: 
            cfg = ConfigParser(interpolation=ExtendedInterpolation())
            cfg.read(config_file)
            firmwareVersion = cfg['serial']['firmwareversion']
            port = cfg['serial']['port']
            baudrate = cfg.getint('serial','baudrate')
            timeout = cfg.getint('serial','timeout')

        self.firmwareVersion = firmwareVersion
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        time.sleep(1)

    def getFirmware(self):
        self.write(30)
        time.sleep(0.5)
        firmName = self.read().decode('utf-8')[:-2]
        
        self.write(31)
        time.sleep(0.5)
        version = self.read().decode('utf-8')[:-2]
    
        return  firmName + "-" + version
        
    def checkFirmware(self):     
        return (self.getFirmware() == self.firmwareVersion)

    def write(self,x):
        if isinstance(x,int):
            self._write_int(x)
        elif isinstance(x,list):
            self._write_list(x)
        
    def _write_int(self,x):
        self.ser.write(x.to_bytes(8,'big'))
        self.ser.flush()
    
    def __write_list(self,lst):
        for x in lst: r = self.ser.write(x.to_bytes(8,'big'))
        self.ser.flush()
    
    def _write_list(self,lst):
        barray = bytearray(lst)
        self.ser.write(barray) 
        self.ser.flush()
 
    def read(self):
        return self.ser.readline()
    
    def off(self):
        self.write([SET_STATE,PIN_OFF])

    def inject(self):
        self.write([SET_STATE,PIN_INJECT])
    
    def flush(self):
        self.write([SET_STATE,PIN_FLUSH])
    
    def stimulus(self):
        self.write([SET_STATE,PIN_STIMULUS])
    
    def pulse(self,pulse_on,pulse_off,num_pulses):
        self.set_number_of_patterns(2)
        self.load_sequence([PIN_STIMULUS,PIN_OFF])
        self.load_intervals([pulse_on,pulse_off])
        self.load_repeats(num_pulses)
        self.trigger_sequence()

    def set_number_of_patterns(self,num_patterns):
        self.write([SET_NUM_PATTERNS,num_patterns])

    def load_sequence(self,seq):
        msg = [SET_PATTERN,0,0]
        for idx,x in enumerate(seq):
            msg[1] = idx
            msg[2] = x
            self.write(msg)

    def load_intervals(self,intervals):
        msg = [SET_TIME_INTERVALS,0,0,0]
        for idx,x in enumerate(intervals):
            msg[1] = idx
            msg[2] = (x >> 8) & 0xff
            msg[3] = x & 0xff
            self.write(msg)

    def load_repeats(self,num_repeats):
        self.write([SET_PATTERN_REPEATS,num_repeats])

    def trigger_sequence(self):
        self.write(TRIGGER_PATTERNS)
     
    

