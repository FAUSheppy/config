import datetime
import sys
import os
import subprocess
import shlex
import re

def hlpath(addition=""):
        return os.path.join(os.path.expanduser("~"),".config/herbstluftwm/"+addition)

def color_remove(s):
        '''removes colorcodes from inputstring'''
        return re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]').sub('',s)

def shexec(s):
        return subprocess.check_output(shlex.split(s),shell=True).decode()

def is_cip():
        u = os.uname()
        return "cip" in u.release or "faui" in u.nodename or "ircbox" in u.nodename

def is_laptop():
        u = os.uname()
        return "laptop" in u.nodename or "atlantismedion" in u.nodename

def error(s):
        with open("herbstlog",'a') as f:
                time = str(datetime.datetime.now().time())[:-7] #cut seconds at the end
                f.write(time + "ERROR" + os.path.basename(__file__) + s)
