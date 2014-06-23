#!/usr/bin/python

#
# This file provides functions to interface with the raspberry pi i/o
#

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
        self.mash_valve = 0
        self.kettle_valve = 0
        self.res_valve = 0
        # pump valves
        self.pump_res_valve = 0
        self.pump_kettle_valve = 0
        # heaters/pumps
        self.pump = 0
        self.heater_kettle = 0
        self.heater_res = 0