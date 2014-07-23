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

print("##########################################")
print("#        Welcome to the Brewery          #")
print("##########################################")
print("")


#XmlParse()

# Create two threads as follows
try:
    controller = Controller()

except:
    print "Error: unable to start controller"

# Use the gui if running from xcode, otherwise run from command line
mode = "LINE"

if mode is "LINE":
    path = raw_input("Please enter your recipe path: ")
    print "You entered ", str(path)
    controller.sys_control.recipe_profile.grain_weight = controller.sys_control.recipe_xml.read_xml(str(path))

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

while 1:
    state = raw_input("Enter a new state at any time to go to that state.\n")
    interrupt_state(str(state))


