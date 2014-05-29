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
        self.input_valve = 0
        self.mash_valve = 0
        self.kettle_valve = 0
        self.res_valve = 0
        self.pump = 0
        self.heater = 0