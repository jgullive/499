#!/usr/bin/python

import time
import thread
from io import *
from sensor_sim import *


class Sensors():

    #############################
    # Outputs
    #############################

    #Input controls
    def input_on(self):
        self.outputs.input_valve = 1
    def input_off(self):
        self.outputs.input_valve = 0
    
    #Pump controls
    def pump_on(self):
        self.outputs.pump = 1
    def pump_off(self):
        self.outputs.pump = 0

    #Heater controls
    def heater_on(self):
        self.outputs.heater = 1
    def heater_off(self):
        self.outputs.heater = 0

    #Mash controls
    def mash_open(self):
        self.outputs.mash_valve = 1
    def mash_closed(self):
        self.outputs.mash_valve = 0

    #Kettle controls
    def kettle_open(self):
        self.outputs.kettle_valve = 1
    def kettle_closed(self):
        self.outputs.kettle_valve = 0

    #Resevoir controls
    def res_open(self):
        self.outputs.res_valve = 1
    def res_closed(self):
        self.outputs.res_valve = 0


    #############################
    # Inputs
    #############################

    #Temperature readings
    def read_mash_temp(self):
        return self.inputs.mash_temp
    
    def read_kettle_temp(self):
        return self.inputs.kettle_temp

    def read_res_temp(self):
        return self.inputs.res_temp

    #Volume readings
    def read_mash_volume(self):
        return self.inputs.mash_volume

    def read_kettle_volume(self):
        return self.inputs.kettle_volume

    def read_res_volume(self):
        return self.inputs.res_volumes
    
    ############################
    # Private
    ############################
    
    def update_sensors(self, threadName, inputs, outputs):
    
        sim_sensors = Simulator(inputs, outputs)
    
        while(1):
            sim_sensors.sim_readings()
            time.sleep(1)
    
    
    def sensor_loop(self, threadName):
        print "entering main sensor loop..."
        #self.input_on()
        time.sleep(0.1)
        #self.input_off()
        #self.heater_on()
        while 1:
            print "kettle (temp, vol): (%0.1f, %0.1f)" % (self.read_kettle_temp(), self.read_kettle_volume())
            time.sleep(1)

    def sensors_run(self):
        print "Starting sensors threads..."
        try:
            thread.start_new_thread( self.update_sensors, ("Sensors_update", self.inputs, self.outputs))
            thread.start_new_thread( self.sensor_loop, ("Sensor_loop", ))
        
        except:
            print "!~Could not start sensors thread~!"

    
    def __init__(self):
        
        #print "initializing sensors..."
        self.inputs = Inputs()
        self.outputs = Outputs()


