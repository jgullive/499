import thread
import time
import sys


from controller import *
from xmlparse import *
from secondthread import print_time
from database import setupDB

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


# Use the gui if running from xcode, otherwise run from command line
mode = "LINE"

if mode is "LINE":
    path = sys.argv
    self.sys_control.recipe_profile.grain_weight = self.sys_control.recipe_xml.read_xml(path)
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