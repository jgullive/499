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
    #Note that the system valve is manual and thus should not be controlled by software
    def input_system_on(self):
        self.outputs.input_system_valve = 1
    def input_system_off(self):
        self.outputs.input_system_valve = 0
    
    def input_kettle_on(self):
        self.outputs.input_kettle_valve = 1
    def input_kettle_off(self):
        self.outputs.input_kettle_valve = 0
    
    def input_res_on(self):
        self.outputs.input_res_valve = 1
    def input_res_off(self):
        self.outputs.input_res_valve = 0
    
    
    #Pump controls
    def pump_on(self):
        self.outputs.pump = 1
    def pump_off(self):
        self.outputs.pump = 0
    
    def pump_res(self):
        self.mash_open()
        self.pump_kettle_valve = 0
        self.pump_res_valve = 1
        sleep(3)
        self.pump_on()
    
    def pump_kettle(self):
        self.mash_open()
        self.pump_kettle_valve = 1
        self.pump_res_valve = 0
        sleep(3)
        self.pump_on()
    
    def stop_pumping(self):
        self.pump_off()
        self.mash_closed()
        self.pump_kettle_valve = 0
        self.pump_res_valve = 0
    

    #Heater controls
    def heater_kettle_on(self):
        self.outputs.heater_kettle = 1
    def heater_kettle_off(self):
        self.outputs.heater_kettle = 0

    def heater_res_on(self):
        self.outputs.heater_res = 1
    def heater_res_off(self):
        self.outputs.heater_res = 0
    
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
        return self.inputs.res_volume
    
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
            self.no_update = 1
            if self.kettle_temp is not self.read_kettle_temp() or self.kettle_volume is not self.read_kettle_volume():
                print "kettle (temp, vol): (%0.1f, %0.1f)" % (self.read_kettle_temp(), self.read_kettle_volume())
                self.no_update = 0
                self.kettle_temp = self.read_kettle_temp()
                self.kettle_volume = self.read_kettle_volume()
            if self.mash_temp is not self.read_mash_temp() or self.mash_volume is not self.read_mash_volume():
                print "mash   (temp, vol): (%0.1f, %0.1f)" % (self.read_mash_temp(), self.read_mash_volume())
                self.no_update = 0
                self.mash_temp = self.read_mash_temp()
                self.mash_volume = self.read_mash_volume()
            if self.res_temp is not self.read_res_temp() or self.res_volume is not self.read_res_volume():
                print "res    (temp, vol): (%0.1f, %0.1f)" % (self.read_res_temp(), self.read_res_volume())
                self.no_update = 0
                self.res_temp = self.read_res_temp()
                self.res_volume = self.read_res_volume()
            if self.no_update:
                print "..."
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
        
        # values used to determine whether to print out updated readings or not
        # only used for print purposes
        self.kettle_temp = 0
        self.kettle_volume = 0
        self.mash_temp = 0
        self.mash_volume = 0
        self.res_temp = 0
        self.res_volume = 0
        self.no_update = 1



