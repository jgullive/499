import thread

from secondthread import print_time
from database import setupDB
from sensors import read_sensors
from gui import open_gui

print "We are using python in xcode!"

#open_gui("notAthread")

# Create two threads as follows
try:
    """
    thread.start_new_thread( print_time, ("Thread-1", 2, ) )
    thread.start_new_thread( print_time, ("Thread-2", 4, ) )
    """
    thread.start_new_thread( read_sensors, ("Sensors",))

except:
    print "Error: unable to start thread"

open_gui()

"""
try:
    setupDB()
except:
    print "Error: unable to setup DB"
"""










while 1:
    pass