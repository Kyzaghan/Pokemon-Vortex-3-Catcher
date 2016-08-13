# -*- coding: utf-8 -*-
import logging
import time
from Utils.termcolor import cprint


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class logger:
    def __init__(self):
        self.l = logging
        self.l.basicConfig(filename=time.strftime("%Y-%m-%d") + '.log', format='%(asctime)s %(message)s',level=logging.DEBUG)

    def writelog(self, message, type):
        message = "[" + time.strftime("%d-%m-%Y %H:%M %S") + "]" + message
        if type == "critical":
            cprint(message, 'red', attrs=['bold'])
            self.l.critical(message)
        elif type == "warning":
            cprint(message, 'cyan')
            self.l.warning(message)
        elif type == "error":
            cprint(message, 'red')
            self.l.error(message)
        else:
            cprint(message, 'green')
            self.l.info(message)

