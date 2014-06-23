import thread
import time


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

open_gui(controller.sys_control)

"""
try:
    setupDB()
except:
    print "Error: unable to setup DB"
"""










while 1:
    pass