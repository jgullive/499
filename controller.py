#
# The controller is responsible for changing the system's outputs based
# on the inputs, state, and profile
#


import datetime
import time
import thread
from xmlparse import *
from sensors import *
from profile import *
from string import upper

KETTLE_VOL = 1
RES_VOL = 1
MASH_VOL = 1

class ControlParameters():
    def __init__(self):
        self.systemOn = 0
        self.mash_start_time = 0
        self.lauter_start_time = 0
        self.boil_start_time = 0
        self.boil_temp_reached = 0
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
        
        oldState = ""
        
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
            if newState is not oldState:
                print newState
                oldState = newState
            
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
    
    return "STRIKEINIT"

#
# Kettle/Res fill and heat
#
def kettle_init_state(state, sensors, sys_control):
    #print "KETTLE INIT"
    
    time.sleep(0.5)
    
    temp_kettle_reached = 0
    vol_kettle_reached  = 0
    temp_res_reached    = 0
    vol_res_reached     = 0

    newState = "STRIKEINIT"

    # KETTLE readings
    if sensors.read_kettle_temp() >= sys_control.recipe_profile.mash_temp + 5:
        sensors.heater_kettle_off()
        temp_kettle_reached = 1
    else:
        sensors.heater_kettle_on()
        temp_kettle_reached = 0
    
    if sensors.read_kettle_volume() >= KETTLE_VOL:
        sensors.input_kettle_off()
        vol_kettle_reached = 1
    else:
        sensors.input_kettle_on()
        vol_kettle_reached = 0
    
    # RES readings
    if sensors.read_res_temp() >= sys_control.recipe_profile.mash_temp + 5:
        sensors.heater_res_off()
        temp_res_reached = 1
    else:
        sensors.heater_res_on()
        temp_res_reached = 0
    
    if sensors.read_res_volume() >= RES_VOL:
        sensors.input_res_off()
        vol_res_reached = 1
    else:
        sensors.input_res_on()
        vol_res_reached = 0
    
    # Check for temps and vols reached
    if vol_kettle_reached and temp_kettle_reached:
        if vol_res_reached and temp_res_reached:
            sensors.input_kettle_off()
            sensors.input_res_off()
            sensors.heater_kettle_off()
            sensors.heater_res_off()
            newState = "MASHFILL"

    return (newState)

#
# Fill the mash
#
def mash_fill_state(state, sensors, sys_control):
    #print "MASHFILL"
    
    if sensors.read_mash_volume() < MASH_VOL:
        sensors.kettle_open()
    else:
        sensors.kettle_closed()
        sys_control.mash_start_time = datetime.datetime.now()
        return "MASH"

    return "MASHFILL"

#
# Mash
#
def mash_state(state, sensors, sys_control):
    #print "MASH"
    
    if sensors.read_mash_temp() <= sys_control.recipe_profile.mash_temp:
        sensors.pump_res()
    else:
        sensors.stop_pumping()
    
    # Keep the RES at the required temperature
    if sensors.read_res_temp() >= sys_control.recipe_profile.mash_temp + 5:
        sensors.heater_res_off()
    else:
        sensors.heater_res_on()

    now = datetime.datetime.now()
    diff = now - sys_control.mash_start_time
    if diff.seconds/60 >= sys_control.recipe_profile.mash_time:
        sensors.stop_pumping()
        return "PRELAUTER"

    return "MASH"

#
# Pre-lauter (heat up the res to temp)
#
def res_lauter_temp_state(state, sensors, sys_control):
    #print "PRELAUTER"
    # Bring the RES up to the required lauter temperature
    if sensors.read_res_temp() >= sys_control.recipe_profile.mash_temp + 10:
        sensors.heater_res_off()
        return "LAUTER"
    else:
        sensors.heater_res_on()

    return "PRELAUTER"

#
# Begin lauter
#
def lauter_state(state, sensors, sys_control):
    #print "LAUTER"
    
    # I'm pretty sure we have to do the lauter by time. We don't have any way to tell when the mash is empty
    if sys_control.lauter_start_time is 0:
        sys_control.lauter_start_time = datetime.datetime.now()
    now = datetime.datetime.now()
    diff = now - sys_control.lauter_start_time
    if diff.seconds/60 >= sys_control.recipe_profile.lauter_time:
        sensors.stop_pumping()
        sensors.res_closed()
        return "BOIL"
    else:
        sensors.res_open()
        sensors.pump_kettle()

    return "LAUTER"

#
# Boil
#
def boil_state(state, sensors, sys_control):
    #print "BOIL"
    
    if sensors.read_kettle_temp() > sys_control.recipe_profile.boil_temp:
        if sys_control.boil_temp_reached is 0:
            sys_control.boil_temp_reached = 1
            sys_control.boil_start_time = datetime.datetime.now()
        sensors.heater_kettle_off()
    else:
        sensors.heater_kettle_on()
    
    if sys_control.boil_temp_reached:
        now = datetime.datetime.now()
        diff = now - sys_control.boil_start_time
        if diff.seconds/60 >= sys_control.recipe_profile.mash_time:
            sensors.heater_kettle_off()
            return "COOL"

    return "BOIL"

#
# Cool
#
def cool_state(state, sensors, sys_control):
    #print "COOL"
    
    

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
        self.stateMachine.add_state("STRIKEINIT", kettle_init_state)
        self.stateMachine.add_state("MASHFILL", mash_fill_state)
        self.stateMachine.add_state("MASH", mash_state)
        self.stateMachine.add_state("PRELAUTER", res_lauter_temp_state)
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






