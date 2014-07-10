import thread
import time
import sys


from controller import *
from xmlparse import *
from secondthread import print_time
#from database import setupDB

from gui import open_gui

print "##########################################"
print "#        Welcome to the Brewery          #"
print "##########################################"
print ""

#XmlParse()

# Create two threads as follows
try:
    controller = Controller()

except:
    print "Error: unable to start controller"

time.sleep(2)

# Use the gui if running from xcode, otherwise run from command line
mode = "LINE"

if mode is "LINE":
    path = input("Please enter your recipe path: ")
    print "You entered ", path
    controller.sys_control.recipe_profile.grain_weight = controller.sys_control.recipe_xml.read_xml(path)

   # var = input("Press enter to start the brew ")
    print "Brew started!"
    controller.sys_control.systemOn = 1

else:
    open_gui(controller.sys_control)

"""
try:
    setupDB()
except:
    print "Error: unable to setup DB"
"""










while 1:
    pass


