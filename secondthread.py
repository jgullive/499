#!/usr/bin/python

import thread
import time

# Define a function for the thread
def print_time( threadName, delay):
    print "printing time"
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print "%s: %s" % ( threadName, time.ctime(time.time()) )
