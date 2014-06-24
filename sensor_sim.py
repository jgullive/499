#
# This file simulates the raspberry pi sensor values so that the
# system can be tested without any hardware
#
# The simulator operates under the assumption that it will be run every 1s
#

from io import *
from profile import *

class Simulator():
    
    
    # Calculate initial volumes and max volumes
    def __init__(self, inputs, outputs):
        
        print "initializing simulator..."

        self.inputs = inputs
        self.outputs = outputs
                
        self.flow_rate = 0.5
        self.heat_rate = 1.5
        self.heat_loss = 0.005
        self.inputs_temp = 32

        
        # Poll each sensor reading
    def sim_readings(self):
        #print "simulating sensors..."
        self.sim_mash_volume()
        self.sim_kettle_volume()
        self.sim_res_volume()
    
        self.sim_mash_temp()
        self.sim_kettle_temp()
        self.sim_res_temp()


    ############################################################################

    # Simulate the temperature readings
    def sim_mash_temp(self):
        if self.outputs.kettle_valve:
            self.inputs.mash_temp += \
                self.calc_temp(self.inputs.kettle_temp, self.inputs.mash_temp, \
                          self.flow_rate, self.inputs.mash_volume, 0)
        if self.outputs.res_valve:
            self.inputs.mash_temp += \
                self.calc_temp(self.inputs.res_temp, self.inputs.mash_temp, \
                            self.flow_rate, self.inputs.mash_volume, 0)
        
        if self.outputs.pump_res_valve and self.outputs.pump:
            self.inputs.mash_temp += \
                self.calc_temp(self.inputs.res_temp, self.inputs.mash_temp, \
                               self.flow_rate, self.inputs.mash_volume, 0)

        self.inputs.mash_temp -= self.calc_heat_loss(self.inputs.kettle_temp, self.inputs.kettle_volume)

    def sim_kettle_temp(self):
        if self.outputs.input_kettle_valve:
            self.inputs.kettle_temp += self.calc_temp(self.inputs_temp, self.inputs.kettle_temp, self.flow_rate, self.inputs.kettle_volume, 0)
    
        if self.outputs.heater_kettle:
            if self.inputs.kettle_volume is not 0:
                self.inputs.kettle_temp += self.heat_rate/(0.5*self.inputs.kettle_volume)
            else:
                self.inputs.kettle_temp += self.heat_rate
        
        self.inputs.kettle_temp -= self.calc_heat_loss(self.inputs.kettle_temp, self.inputs.kettle_volume)

    def sim_res_temp(self):
        if self.outputs.input_res_valve:
            self.inputs.res_temp += self.calc_temp(self.inputs_temp, self.inputs.res_temp, self.flow_rate, self.inputs.res_volume, 0)
        
        if self.outputs.heater_res:
            if self.inputs.res_volume is not 0:
                self.inputs.res_temp += self.heat_rate/(0.5*self.inputs.res_volume)
            else:
                self.inputs.res_temp += self.heat_rate
        
        self.inputs.res_temp -= self.calc_heat_loss(self.inputs.res_temp, self.inputs.res_volume)

    def calc_temp(self, new_temp, old_temp, new_vol, old_vol, sh):
        if old_vol > 1:
            #print ">> %0.2f" % ((new_temp - old_temp)*(new_vol)/(old_vol))
            return (0.5*(new_temp - old_temp)*(new_vol)/(old_vol))
        else:
            #print "<< %0.2f" % (new_temp*0.1)
            return new_temp*0.01

    def calc_heat_loss(self, temperature, volume):
        if volume > 1:
            return temperature/volume*self.heat_loss
        elif temperature > (self.heat_loss*0.1):
            return (self.heat_loss*0.1)
        else:
            return 0

    # Simulate the volume readings
    def sim_mash_volume(self):
        if self.outputs.res_valve and self.inputs.res_volume > self.flow_rate:
            self.inputs.mash_volume += self.flow_rate
        if self.outputs.kettle_valve and self.inputs.kettle_volume > self.flow_rate:
            self.inputs.mash_volume += self.flow_rate
        if self.outputs.pump_res_valve and self.outputs.pump and self.inputs.mash_volume > self.flow_rate:
            self.inputs.mash_volume += self.flow_rate
        #print "1: " + str(self.outputs.mash_valve) + " " + str(self.outputs.pump) + " " + str(self.outputs.pump_kettle_valve)
        if self.outputs.mash_valve and self.outputs.pump and (self.outputs.pump_kettle_valve or self.outputs.pump_res_valve):
            #print "empyting mash to kettle"
            if self.inputs.mash_volume > self.flow_rate:
                self.inputs.mash_volume -= self.flow_rate
            else:
                print "Mash is empty, close valve"

    def sim_kettle_volume(self):
        if self.outputs.input_kettle_valve and self.inputs.res_volume > self.flow_rate:
            self.inputs.kettle_volume += self.flow_rate
        #print "2: " + str(self.outputs.mash_valve) + " " + str(self.outputs.pump) + " " + str(self.outputs.pump_kettle_valve)
        if self.outputs.mash_valve and (self.outputs.pump and self.outputs.pump_kettle_valve) and self.inputs.mash_volume > self.flow_rate:
            #print "Filling kettle from mash"
            self.inputs.kettle_volume += self.flow_rate
        if self.outputs.kettle_valve:
            if self.inputs.kettle_volume > self.flow_rate:
                self.inputs.kettle_volume -= self.flow_rate
            else:
                print "Kettle is empty, close valve"

    def sim_res_volume(self):
        if self.outputs.input_res_valve:
            self.inputs.res_volume += self.flow_rate
        if self.outputs.res_valve:
            if self.inputs.res_volume > self.flow_rate:
                self.inputs.res_volume -= self.flow_rate
            else:
                print "Res is empty, close valve"


