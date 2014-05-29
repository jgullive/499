#
# The controller is responsible for changing the system's outputs based
# on the inputs, state, and profile
#

import time
import thread
from xmlparse import *
from sensors import *
from profile import *
from string import upper

class ControlParameters():
    def __init__(self):
        self.systemOn = 0
        self.recipe_xml = XmlParse()
        self.sys_profile = SystemProfile()
        self.recipe_profile = RecipeProfile()


class StateMachine():
    def __init__(self, sensors, sys_control):
        print "Starting state machine..."
        self.sys_control = sys_control
        self.sensors = sensors
        self.handlers = {}
        self.startState = None
        self.endStates = []

    
    def statePrint(self, handler):
        print "state Print"
            
    def add_state(self, name, handler, end_state=0):
        name = upper(name)
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)
    
    def set_start(self, name):
        self.startState = upper(name)
    
    
    def run(self, threadName, cargo):
        
        try:
            handler = self.handlers[self.startState]
            newState = self.startState
        except:
            raise "InitializationError", "must call .set_start() before .run()"
        
        if not self.endStates:
            raise  "InitializationError", "at least one state must be an end_state"
        
        while 1:
            while system_freeze(newState, self.sensors, self.sys_control) is "FREEZE":
                pass
            handler = self.handlers[upper(newState)]
            newState = handler(newState, self.sensors, self.sys_control)
            
            if upper(newState) in self.endStates:
                newState = system_freeze(newState, self.sensors, self.sys_control)
                handler = self.handlers[upper(newState)]
                newState = handler(newState, self.sensors, self.sys_control)
                break


#
# Emergency system freeze. While enabled no pumps/heaters/valves are on
# Can be enabled by either the user or the system. Currently there is no way
# to recover from the system initiating the freeze
#
def system_freeze(state, sensors, sys_control):
    
    if state is "FREEZE":
        raise "FreezeError", "the system has automatically frozen itself to avoid danger"
    if not sys_control.systemOn:
        sensors.outputs.input_valve = 0
        sensors.outputs.mash_valve = 0
        sensors.outputs.kettle_valve = 0
        sensors.outputs.res_valve = 0
        sensors.outputs.pump = 0
        sensors.outputs.heater = 0
        return ("FREEZE")
    else:
        return (state)

#
# Initialize system setup
#
def initialize_state(state, sensors, sys_control):
    print "INIT"


    sys_control.recipe_profile.grain_weight = sys_control.recipe_xml.parse_xml()
    sys_control.sys_profile.calibrate_system(sys_control.recipe_profile)
    print "grain weight: %0.2f" % sys_control.recipe_profile.grain_weight
    
    return "KETTLEINIT"

#
# Kettle fill and heat
#
def kettle_init_state(state, sensors, sys_control):
    #print "KETTLE FILL"
    
    time.sleep(0.5)
    
    temp_reached = 0
    vol_reached = 0

    newState = "KETTLEINIT"

    if sensors.read_kettle_temp() >= 37:
        sensors.heater_off()
        temp_reached = 1
    else:
        sensors.heater_on()
        temp_reached = 0
    
    if sensors.read_kettle_volume() >= 15:
        sensors.input_off()
        vol_reached = 1
    else:
        sensors.input_on()
        vol_reached = 0
            
    if vol_reached and temp_reached:
        newState = "RESFILL1"

    return (newState)


#
# Fill the resevoir for mash
#

def res_fill_mash_state(state, sensors, sys_control):
    print "RESFILL1"

    return "MASHFILL"
#
# Fill the mash
#
def mash_fill_state(state, sensors, sys_control):
    print "MASHFILL"

    return "MASH"
#
# Mash
#
def mash_state(state, sensors, sys_control):
    print "MASH"

    return "PRELAUTER"

#
# Pre-lauter (heat up the kettle to temp)
#
def kettle_lauter_temp_state(state, sensors, sys_control):
    print "PRELAUTER"

    return "RESFILL2"

#
# Fill the resevoir for lauter
#
def res_fill_lauter_state(state, sensors, sys_control):
    print "RESFILL2"

    return "LAUTER"

#
# Begin lauter
#
def lauter_state(state, sensors, sys_control):
    print "LAUTER"

    return "BOIL"

#
# Boil
#
def boil_state(state, sensors, sys_control):
    print "BOIL"

    return "COOL"

#
# Cool
#
def cool_state(state, sensors, sys_control):
    print "COOL"

    return "END"
#
# The brew is done. Handle any final tidying up
#
def final_state(state, sensors, sys_control):
    print "END STATE"
    
#print "The value of counter is: %d" % args

    return("END")



###############################################
#
# Controller Class
#
###############################################
class Controller():
    
    def __init__(self):
        
        print "Starting controller..."
        
        self.sensors = Sensors()
        self.sys_control = ControlParameters()
        self.stateMachine = StateMachine(self.sensors, self.sys_control)
        
        self.stateMachine.add_state("FREEZE", system_freeze)
        self.stateMachine.add_state("INIT", initialize_state)
        self.stateMachine.add_state("KETTLEINIT", kettle_init_state)
        self.stateMachine.add_state("RESFILL1", res_fill_mash_state)
        self.stateMachine.add_state("MASHFILL", mash_fill_state)
        self.stateMachine.add_state("MASH", mash_state)
        self.stateMachine.add_state("PRELAUTER", kettle_lauter_temp_state)
        self.stateMachine.add_state("RESFILL2", res_fill_lauter_state)
        self.stateMachine.add_state("LAUTER", lauter_state)
        self.stateMachine.add_state("BOIL", boil_state)
        self.stateMachine.add_state("COOL", cool_state)
        self.stateMachine.add_state("END", final_state, end_state=1)
        self.stateMachine.set_start("INIT")
        
        try:
            thread.start_new_thread( self.stateMachine.run, ("State_machine", 1))
        
        except:
            print "!~Could not start state machine thread~!"
        
        self.sensors.sensors_run()
        
        print "Finished controller setup!"


















