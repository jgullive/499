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



MASH_FLT_PIN    = 23
KETTLE_FLT_PIN  = 2
RES_FLT_PIN     = 3

TEMP_PIN        = 4

HOP_PIN_A       = 14
HOP_PIN_B       = 15
HOP_PIN_C       = 18
HOP_PIN_D       = 24
        
CIRC_VLV_PIN    = 17
SPRG_VLV_PIN    = 27
KETTLE_VLV_PIN  = 22
RES_VLV_PIN     = 10
KETTLE_IN_PIN   = 9
RES_IN_PIN      = 11

PUMP_PIN        = 25
KETTLE_HT_PIN   = 8
RES_HT_PIN      = 7

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












