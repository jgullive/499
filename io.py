#!/usr/bin/python

#
# This file provides functions to interface with the raspberry pi i/o
#

import RPi.GPIO as GPIO
import os
import glob
import time
import subprocess


GPIO.VERSION

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

currentCommandStep = 0

MASH_FLT_PIN    = 23 # yellow dash dot dash
KETTLE_FLT_PIN  = 2  # yellow dash dot dot dash
RES_FLT_PIN     = 3  # yellow dash dot dot dot dash

TEMP_PIN        = 4  # yellow dash

HOP_PIN_A       = 14 # yellow dot
HOP_PIN_B       = 15 # yellow dot dot
HOP_PIN_C       = 18 # yellow dot dot dot
HOP_PIN_D       = 24 # yellow dot dot dot dot
        
CIRC_VLV_PIN    = 17 # red dot
SPRG_VLV_PIN    = 27 # red dot dot
KETTLE_VLV_PIN  = 22 # red dot dot dot
RES_VLV_PIN     = 10 # red dot dash
KETTLE_IN_PIN   = 9  # red dot dot dash
RES_IN_PIN      = 11 # red dot dot dot dash

PUMP_PIN        = 25 # yellow dot dot dash dot dot
KETTLE_HT_PIN   = 8  # red dot dot dash dot dot
RES_HT_PIN      = 7  # red dot dash dot

MASH_ID   = "597aa17"
KETTLE_ID = "54769b8"
RES_ID    = "598ffd6"

#Configure the I/O
GPIO.setup(MASH_FLT_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(KETTLE_FLT_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(RES_FLT_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

GPIO.setup(HOP_PIN_A, GPIO.OUT)
GPIO.setup(HOP_PIN_B, GPIO.OUT)
GPIO.setup(HOP_PIN_C, GPIO.OUT)
GPIO.setup(HOP_PIN_D, GPIO.OUT)

GPIO.setup(CIRC_VLV_PIN, GPIO.OUT)
GPIO.setup(SPRG_VLV_PIN, GPIO.OUT)
GPIO.setup(RES_VLV_PIN, GPIO.OUT)
GPIO.setup(KETTLE_VLV_PIN, GPIO.OUT)
GPIO.setup(RES_IN_PIN, GPIO.OUT)
GPIO.setup(KETTLE_IN_PIN, GPIO.OUT)

GPIO.setup(PUMP_PIN, GPIO.OUT)
GPIO.setup(KETTLE_HT_PIN, GPIO.OUT)
GPIO.setup(RES_HT_PIN, GPIO.OUT)


#def printfunc(channel):
#
#    if(GPIO.input(23) == 1):
#        print("Level not reached!")
#    else:
#        print("Level reached!")
    
class Inputs():
    def __init__(self):
        self.mash_temp = 1
        self.kettle_temp = 0
        self.res_temp = 0

        # bool for if the required volume is reached
        self.mash_volume = 0
        self.kettle_volume = 0
        self.res_volume = 0

class Outputs():
    
    def __init__(self):
        # in valves
        self.input_kettle_valve = 0
        self.input_res_valve = 0
        # out valves
        self.mash_valve = 0     #-----Not used anymore
        self.kettle_valve = 0
        self.res_valve = 0
        # pump valves
        self.pump_res_valve = 0
        self.pump_kettle_valve = 0
        # heaters/pumps
        self.pump = 0
        self.heater_kettle = 0
        self.heater_res = 0

        
def sttepperRotate(steps, direction):

    while (steps != 0): 
        #Outputs current step to motor PORT

        if currentCommandStep is 0:
            GPIO.output(HOP_PIN_A, 1)            
            GPIO.output(HOP_PIN_B, 0)            
            GPIO.output(HOP_PIN_C, 0)            
            GPIO.output(HOP_PIN_D, 0)            
        elif currentCommandStep is 1:
            GPIO.output(HOP_PIN_A, 0)            
            GPIO.output(HOP_PIN_B, 1)            
            GPIO.output(HOP_PIN_C, 0)            
            GPIO.output(HOP_PIN_D, 0)            
        elif currentCommandStep is 2:
            GPIO.output(HOP_PIN_A, 0)            
            GPIO.output(HOP_PIN_B, 0)            
            GPIO.output(HOP_PIN_C, 1)            
            GPIO.output(HOP_PIN_D, 0)            
        elif currentCommandStep is 3:
            GPIO.output(HOP_PIN_A, 0)            
            GPIO.output(HOP_PIN_B, 0)            
            GPIO.output(HOP_PIN_C, 0)            
            GPIO.output(HOP_PIN_D, 1)            

        currentCommandStep = currentCommandStep + direction  
        steps = steps - 1  #One step closer to the goal 
                                               
        # These if statements keep currentStep between 0 and 3 
        if (currentCommandStep < 0): 
            currentCommandStep = 3 
        elif(currentCommandStep > 3): 
            currentCommandStep = 0 
        time.sleep(0.020)
                                                                                   

class IO():

    def float_update(self):

        if(GPIO.input(MASH_FLT_PIN) != self.inputs.mash_volume):
            self.inputs.mash_volume = GPIO.input(MASH_FLT_PIN)
        #    print "Mash level changed to ", self.inputs.mash_volume

        if(GPIO.input(KETTLE_FLT_PIN) != self.inputs.kettle_volume):
            self.inputs.kettle_volume = GPIO.input(KETTLE_FLT_PIN)
        #    print "Kettle level changed to ", self.inputs.kettle_volume

        if(GPIO.input(RES_FLT_PIN) != self.inputs.res_volume):
            self.inputs.res_volume = GPIO.input(RES_FLT_PIN)
        #    print "Res level changed to ", self.inputs.res_volume

    def temp_update(self):

        for device in self.device_file:
            #f = open(device, 'r')
            #lines = f.readlines()
            #f.close()

            catdata = subprocess.Popen(['cat',device], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out,err = catdata.communicate()
            out_decode = out.decode('utf-8')
            lines = out_decode.split('\n')
            #print lines
            while 1:
                if (lines[0].strip()[-3:] == 'YES') or (lines[0].strip()[-2:] == 'NO'):
                    break
                #time.sleep(0.02)
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                if MASH_ID in device:
                    self.inputs.mash_temp = temp_f
                if KETTLE_ID in device:
                    self.inputs.kettle_temp = temp_f
                if RES_ID in device:
                    self.inputs.res_temp = temp_f
         #       print "Current temp is",  temp_c, " ", temp_f, " ", device

    def output_update(self):
        # in valves
        GPIO.output(KETTLE_IN_PIN, self.outputs.input_kettle_valve)
        GPIO.output(RES_IN_PIN, self.outputs.input_res_valve)
        # out valves
        GPIO.output(KETTLE_VLV_PIN, self.outputs.kettle_valve)
        GPIO.output(RES_VLV_PIN, self.outputs.res_valve)
        # pump valves
        GPIO.output(CIRC_VLV_PIN, self.outputs.pump_res_valve)
        GPIO.output(SPRG_VLV_PIN, self.outputs.pump_kettle_valve)
        # heaters/pumps
        GPIO.output(PUMP_PIN, self.outputs.pump)
        GPIO.output(KETTLE_HT_PIN, self.outputs.heater_kettle)
        GPIO.output(RES_HT_PIN, self.outputs.heater_res)

    def run(self):
        print("Starting the REAL sensor loop...")

        while True:
            self.float_update()
            self.temp_update()
            self.output_update()
            print "!!!"
            #for device in self.device_file:
            #    f = open(device, 'r')
            #    lines = f.readlines()
            #    f.close()
            #    print lines
            #    while 1:
            #        if (lines[0].strip()[-3:] == 'YES') or (lines[0].strip()[-2:] == 'NO'):
            #            break
            time.sleep(0.5)
        GPIO.cleanup()

    def __init__(self, inputs, outputs):

        print("Initializing IO...")
        self.inputs  = inputs
        self.outputs = outputs
        self.device_file = []

        #Setup the temp sensor readings
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        base_dir = '/sys/bus/w1/devices/'
        dirs = os.walk(base_dir).next()
        for d in dirs[1]:
            if d.startswith('28'):
                self.device_file.append(base_dir + d + '/w1_slave')

        #print self.device_file

        # Removed because I was having trouble getting the callback to work properly and the temp sensors need to be polled anyway...
        #GPIO.add_event_detect(MASH_FLT_PIN, GPIO.BOTH, callback = IO.float_update, bouncetime = 100)












