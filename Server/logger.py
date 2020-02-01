import datetime as dt
import time

start = None
logfile = None
date = dt.datetime.now().date()


def begin(delay=0):
    global start
    time.sleep(delay)
    start = dt.datetime(dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day, dt.datetime.now().hour,
                        dt.datetime.now().minute, dt.datetime.now().second)
    return 0


def end(delay=0):
    global start
    time.sleep(delay)
    start = None
    return 0


def startlogfile(path):
    global logfile
    with open(path + "Log " + str(date), 'w') as file:
        file.write('Log Started: ' + str(dt.datetime.today()))
        file.write('\n')
        file.write('+---------------------------------------+')
        file.write('\n')
    logfile = path + "Log " + str(date)


def log(a=""):
    global logfile
    with open(logfile, 'a') as file:
        file.write(str(dt.datetime.now().time()) + "| Logged: " + str(a) + '\n')
    return 0


def endlogfile():
    global logfile
    with open(logfile, 'a') as file:
        file.write('+---------------------------------------+')
        file.write('\n')
        file.write('Log Ended: ' + str(dt.datetime.today()))
