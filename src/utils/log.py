import sys 
# sys.path.append('../config')

import config

import logging
from datetime import datetime

import pprint

class Log:
    @staticmethod
    def configLogger():
        now = datetime.now()
        date_time = now.strftime("%Y.%m.%d")
        logging.basicConfig(filename='../logs/api_' + date_time + '.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

    @staticmethod
    def debug(log):
        if config.RECORD_LOG:
            Log.configLogger()
            logging.debug(log)
        else:
            pprint.pprint(log)

    @staticmethod
    def error(log):
        if config.RECORD_LOG:
            Log.configLogger()
            logging.error(log)
        else:
            pprint.pprint(log)

    @staticmethod
    def info(log):
        if config.RECORD_LOG:
            Log.configLogger()
            logging.info(log)
        else:
            pprint.pprint(log)