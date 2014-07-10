

import RPi.GPIO as GPIO


GPIO.VERSION
    
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


MASH_FLT_PIN    = 23
KETTLE_FLT_PIN  = 2
RES_FLT_PIN     = 3

TEMP_PIN        = 4

HOP_PIN_A       = 14
HOP_PIN_B       = 15
HOP_PIN_C       = 18
HOP_PIN_D       = 24

CIRC_VLV_PIN    = 17
SPRG_VLV_PIN    = 27
KETTLE_VLV_PIN  = 22
RES_VLV_PIN     = 10
KETTLE_IN_PIN   = 9
RES_IN_PIN      = 11

PUMP_PIN        = 25
KETTLE_HT_PIN   = 8
RES_HT_PIN      = 7

MASH_ID   = "597aa17"
KETTLE_ID = "54769b8"
RES_ID    = "598ffd6"


def output_test(PIN):
    GPIO.output(PIN, 1)
    input("Press enter to continue to the next test. ")
    GPIO.output(PIN, 0)


class io_test():

    def __init__(self):
        print "##########################################"
        print "#      Welcome to the Brewery Test       #"
        print "##########################################"
        print ""
        
        #Configure the I/O
        GPIO.setup(MASH_FLT_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(KETTLE_FLT_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(RES_FLT_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        
        GPIO.setup(HOP_PIN_A, GPIO.OUT)
        GPIO.setup(HOP_PIN_B, GPIO.OUT)
        GPIO.setup(HOP_PIN_C, GPIO.OUT)
        GPIO.setup(HOP_PIN_D, GPIO.OUT)
        
        GPIO.setup(CIRC_VLV_PIN, GPIO.OUT)
        GPIO.setup(SPRG_VLV_PIN, GPIO.OUT)
        GPIO.setup(RES_VLV_PIN, GPIO.OUT)
        GPIO.setup(KETTLE_VLV_PIN, GPIO.OUT)
        GPIO.setup(RES_IN_PIN, GPIO.OUT)
        GPIO.setup(KETTLE_IN_PIN, GPIO.OUT)
        
        GPIO.setup(PUMP_PIN, GPIO.OUT)
        GPIO.setup(KETTLE_HT_PIN, GPIO.OUT)
        GPIO.setup(RES_HT_PIN, GPIO.OUT)


    def run_tests():
        
        run_test = input("Press 1 to run hopperator tests: ")
        print ""

        if run_test:
            print "Testing HOP_PIN_A"
            output_test(HOP_PIN_A)
            print "Testing HOP_PIN_B"
            output_test(HOP_PIN_B)
            print "Testing HOP_PIN_C"
            output_test(HOP_PIN_C)
            print "Testing HOP_PIN_D"
            output_test(HOP_PIN_D)


        run_tests = input("Press 1 to run valve tests: ")
        print ""

        if run_tests:
            print "Testing CIRC_VLV_PIN"
            output_test(CIRC_VLV_PIN)
            print "Testing SPRG_VLV_PIN"
            output_test(SPRG_VLV_PIN)
            print "Testing RES_VLV_PIN"
            output_test(RES_VLV_PIN)
            print "Testing KETTLE_VLV_PIN"
            output_test(KETTLE_VLV_PIN)
            print "Testing RES_IN_PIN"
            output_test(RES_IN_PIN)
            print "Testing KETTLE_IN_PIN"
            output_test(KETTLE_IN_PIN)

        input("Press 1 to run high-voltage tests: ")
        print ""

        if run_tests:
            print "Testing PUMP_PIN"
            output_test(PUMP_PIN)
            print "Testing KETTLE_HT_PIN"
            output_test(KETTLE_HT_PIN)
            print "Testing RES_HT_PIN"
            output_test(RES_HT_PIN)

        print "End of test suite."
        print "Thanks for playing!"

