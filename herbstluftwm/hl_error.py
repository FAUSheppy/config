import datetime
import sys
import os

def error(s):
        with open("herbstlog",'a') as f:
                time = str(datetime.datetime.now().time())[:-7] #cut seconds at the end
                f.write(time + "ERROR" + os.path.basename(__file__) + s)
