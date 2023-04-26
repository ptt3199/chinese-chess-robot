import logging

logging.basicConfig(filename='Log/LogFile.log', level=logging.DEBUG, format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


class Logger:
    def __init__(self, class_name):
        self.className = class_name

    def info(self, message):
        logging.info(self.className + ": " + message)

