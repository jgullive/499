#!/usr/bin/python

import time

def read_sensors( threadName):
    while(1):
        print "reading sensor values..."
        update_mash()
        update_kettle()
        update_resevoir()

        time.sleep(1)

def update_mash():
    print "mash temp: %s" % inputs['mash_temp']

def update_kettle():
    print "kettle temp: %s" % inputs['kettle_temp']

def update_resevoir():
    print "res temp: %s" % inputs['res_temp']