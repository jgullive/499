import thread
import time
import sys
import logging
import os


from controller import *
from xmlparse import *
from secondthread import print_time
from logger import *
#from database import setupDB

from gui import open_gui

logger = Logger()
logger.logprint('stuff stuf stuff', 'debug')

print "##########################################"
print "#        Welcome to the Brewery          #"
print "##########################################"
print ""

#stepper_rotate(50, 1)

#XmlParse()

# Create two threads as follows
try:
    controller = Controller()

except:
    print "Error: unable to start controller"

# Use the gui if running from xcode, otherwise run from command line
mode = "LINE"

if mode is "LINE":
    path = input("Please enter your recipe path: ")
    print "You entered ", path
    controller.sys_control.recipe_profile.grain_weight = controller.sys_control.recipe_xml.read_xml(path)

   # var = input("Press enter to start the brew ")
    print "Brew started!"
    controller.sys_control.systemOn = 1
    controller.sensors.sensors_run()

else:
    open_gui(controller.sys_control)

"""
try:
    setupDB()
except:
    print "Error: unable to setup DB"
"""

time.sleep(2)
interrupt_state("FREEZE")
time.sleep(2)
interrupt_state("MASH")
time.sleep(2)
interrupt_state("BOIL")

while 1:
    #state = input("Hit 1 to stop the brew: "
    #if state is 1:
    #    oldState = controller.sys_control.
    pass


