#!/usr/bin/python


inputs = {'mash_temp': 0, 'kettle_temp': 0, 'res_temp': 0, 'mash_volume': 0, 'kettle_volume': 0, 'res_volume': 0};
outputs = {'mash_valve': 0, 'kettle_valve': 0, 'res_valve': 0, 'pump': 0, 'heater': 0};


#############################
# Outputs
#############################

#Pump controls
def pump_on():
    outputs['pump'] = 1

def pump_off():
    outputs['pump'] = 0

#Heater controls
def heater_on():
    outputs['heater'] = 1

def heater_off():
    outputs['heater'] = 0

#Mash controls
def mash_open():
    outputs['mash_valve'] = 1
def mash_closed():
    outputs['mash_valve'] = 0

#Kettle controls
def kettle_open():
    outputs['kettle_valve'] = 1

def kettle_closed():
    outputs['kettle_valve'] = 0

#Resevoir controls
def res_open():
    outputs['res_valve'] = 1

def res_closed():
    outputs['res_valve'] = 0



#############################
# Inputs
#############################

