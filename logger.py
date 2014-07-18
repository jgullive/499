import logging
import os
import datetime
import sys


d = './logs'
if not os.path.exists(d):
    os.makedirs(d)
    print 'no directory'
else:
    print 'found directory'


now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
log_file = '/brewlog_'+now+'.log'
# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=d+log_file,
                        filemode='w')

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

class Logger():

    def logprint(self, message, level='info'):
        if level is 'debug':
            logging.debug(message)
        elif level is 'info':
            logging.info(message)
        elif level is 'warning':
            logging.warning(message)
        elif level is 'error':
            logging.error(message)
        else:
            logging.error('message level unknown: ',message) 




logger = Logger()
logger.logprint('Hello world!', 'debug')
