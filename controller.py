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
from logger import *

KETTLE_VOL = 1
RES_VOL = 1
MASH_VOL = 1
MASH_FILL_TIME = 0
HEAT_LOSS = 15

my_interrupt_state = "none"

class ControlParameters():
    def __init__(self):
        self.systemOn = 0
        self.fill_start_time = 0
        self.mash_start_time = 0
        self.lauter_start_time = 0
        self.boil_start_time = 0
        self.boil_temp_reached = 0
        self.recipe_xml = XmlParse()
        self.sys_profile = SystemProfile()
        self.recipe_profile = RecipeProfile()

        self.hop1 = 0
        self.hop2 = 0
        self.hop3 = 0
        self.hop4 = 0


class StateMachine():
    def __init__(self, sensors, sys_control):
        self.logger = Logger()
        self.logger.logprint("Initializing state machine...")
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
        global my_interrupt_state
        
        try:
            handler = self.handlers[self.startState]
            newState = self.startState
        except:
            raise "InitializationError", "must call .set_start() before .run()"
        
        if not self.endStates:
            raise  "InitializationError", "at least one state must be an end_state"
        
        while 1:
            while system_off(newState, self.sensors, self.sys_control) is "OFF":
                pass
            if my_interrupt_state is not "none":
                normal_state = newState
                newState = my_interrupt_state
                my_interrupt_state = 'none'
                outputs_off(self.sensors)
            if upper(newState) in self.handlers:
                handler = self.handlers[upper(newState)]
                newState = handler(newState, self.sensors, self.sys_control)
                if newState is not oldState:
                    self.logger.logprint(newState)
                    if newState is "FREEZE":
                        self.logger.logprint("The system has been frozen!", 'warning')
                    oldState = newState
            
                if upper(newState) in self.endStates:
                    newState = system_off(newState, self.sensors, self.sys_control)
                    handler = self.handlers[upper(newState)]
                    newState = handler(newState, self.sensors, self.sys_control)
                    break
            else:
                self.logger.logprint("Unknown state entered!", 'warning')
                newState = normal_state


def interrupt_state(new_state):
    global my_interrupt_state

    my_interrupt_state = new_state

def outputs_off(sensors):

    sensors.outputs.input_valve = 0
    sensors.outputs.mash_valve = 0
    sensors.outputs.kettle_valve = 0
    sensors.outputs.res_valve = 0
    sensors.outputs.pump = 0
    sensors.outputs.heater = 0

#
# Emergency system freeze. While enabled no pumps/heaters/valves are on
# Can be enabled by either the user or the system. Currently there is no way
# to recover from the system initiating the freeze
#
def system_freeze(state, sensors, sys_control):
    outputs_off(sensors) 
    return ("FREEZE")


def system_off(state, sensors, sys_control):


    if not sys_control.systemOn:
        outputs_off(sensors)
        return ("OFF")
    else:
        return(state)

#
# Initialize system setup
#
def initialize_state(state, sensors, sys_control):
    
    Logger().logprint("INIT")


    sys_control.recipe_xml.parse_xml(sys_control.recipe_profile)
    sys_control.sys_profile.calibrate_system(sys_control.recipe_profile)
    Logger().logprint("Grain weight: %0.2f" % sys_control.recipe_profile.grain_weight)
    
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
    if sensors.read_kettle_volume() >= KETTLE_VOL:
        sensors.input_kettle_off()
        vol_kettle_reached = 1
        if sensors.read_kettle_temp() >= sys_control.recipe_profile.mash_temp + HEAT_LOSS -100:
            sensors.heater_kettle_off()
            temp_kettle_reached = 1
        else:
            sensors.heater_kettle_on()
            temp_kettle_reached = 0
    
    else:
        sensors.input_kettle_on()
        vol_kettle_reached = 0
        sensors.heater_kettle_off()
        temp_kettle_reached = 1
    
    # RES readings
    if sensors.read_res_volume() >= RES_VOL:
        sensors.input_res_off()
        vol_res_reached = 1
        if sensors.read_res_temp() >= sys_control.recipe_profile.mash_temp + HEAT_LOSS -100:
            sensors.heater_res_off()
            temp_res_reached = 1
        else:
            sensors.heater_res_on()
            temp_res_reached = 0
    else:
        sensors.input_res_on()
        vol_res_reached = 0
        sensors.heater_res_off()
        temp_res_reached = 1
    
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

    # We can't sense when the mash is filled because the float
    # switches are just on/off and the mash one is being used for overflow.
    # Could possibly change this in the future. For now its timed.
    if sys_control.fill_start_time is 0:
        sys_control.fill_start_time = datetime.datetime.now()
    
    now = datetime.datetime.now()
    diff = now - sys_control.fill_start_time
    if float(diff.seconds)/60 < MASH_FILL_TIME:
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
    if sensors.read_res_temp() >= sys_control.recipe_profile.mash_temp + HEAT_LOSS:
        sensors.heater_res_off()
    else:
        sensors.heater_res_on()

    now = datetime.datetime.now()
    if not sys_control.mash_start_time:
        sys_control.mash_start_time = now
    diff = now - sys_control.mash_start_time
    if float(diff.seconds)/60 > sys_control.recipe_profile.mash_time:
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
    if float(diff.seconds)/60 > sys_control.recipe_profile.lauter_time:
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
        if sys_control.boil_start_time is 0:
            sys_control.boil_start_time = datetime.datetime.now()
        now = datetime.datetime.now()
        diff = now - sys_control.boil_start_time
        if float(diff.seconds)/60 > sys_control.recipe_profile.boil_time:
            sensors.heater_kettle_off()
            return "COOL"
        # Hop dispensing logic
        #print 'boil time information ', sys_control.hop1, ' ', float(diff.seconds)/60, ' ', (sys_control.recipe_profile.boil_time - sys_control.recipe_profile.hops1) 
        if  (sys_control.hop1 is 0) and (float(diff.seconds)/60 > (sys_control.recipe_profile.boil_time - sys_control.recipe_profile.hops1)):
            sensors.hop_addition()
            sys_control.hop1 = 1
        if (sys_control.hop2 is 0) and (float(diff.seconds)/60 > (sys_control.recipe_profile.boil_time - sys_control.recipe_profile.hops2)):
            sensors.hop_addition()
            sys_control.hop2 = 1
        if (sys_control.hop3 is 0) and (float(diff.seconds)/60 > (sys_control.recipe_profile.boil_time - sys_control.recipe_profile.hops3)):
            sensors.hop_addition()
            sys_control.hop3 = 1
        if (sys_control.hop4 is 0) and (float(diff.seconds)/60 > (sys_control.recipe_profile.boil_time - sys_control.recipe_profile.hops4)):
            sensors.hop_addition()
            sys_control.hop4 = 1

    return "BOIL"

#
# Cool
#
def cool_state(state, sensors, sys_control):
    #print "COOL"
    
    print("The cooling stage must be performed manually. System shutting off now.")

    return "END"
#
# The brew is done. Handle any final tidying up
#
def final_state(state, sensors, sys_control):
    print "END STATE"
    
    return("END")



###############################################
#
# Controller Class
#
###############################################
class Controller():
    
    def __init__(self):
        
        
        self.logger = Logger()
        self.logger.logprint('Initializing controller...')
        self.sensors = Sensors()
        self.sys_control = ControlParameters()
        self.stateMachine = StateMachine(self.sensors, self.sys_control)

        
        self.stateMachine.add_state("FREEZE", system_freeze)
        self.stateMachine.add_state("OFF", system_freeze)
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
            self.logger.logprint("!~Could not start state machine thread~!", 'error')
        






