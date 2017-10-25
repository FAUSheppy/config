import datetime
import string
import re
import sys
import os
import subprocess
import shlex
import re
from hl_constants import *

def hlpath(addition=""):
        return os.path.join(os.path.expanduser("~"),".config/herbstluftwm/"+addition)

def color_remove(s):
        '''removes colorcodes from inputstring'''
        return re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]').sub('',s)

def shexec(s):
        return subprocess.check_output(shlex.split(s),shell=False).decode()

def is_cip():
        u = os.uname()
        return "cip" in u.release or "faui" in u.nodename or "ircbox" in u.nodename

def is_laptop():
        u = os.uname()
        return "laptop" in u.nodename or "atlantismedion" in u.nodename

def error(s):
        with open(hlpath("herbstlog"),'a') as f:
                time = str(datetime.datetime.now().time())[:-7] #cut seconds at the end
                f.write(time + " ERROR: " + os.path.basename(__file__) + ' ' +s +'\n')

def color_panel(s,hex_code,seper=True):
        if type(hex_code)==int:
                hex_code = hex(hex_code)
        hex_code = hex_code.lstrip('0x')
        if seper:
            sep=color_panel(SEP,DEFAULT_FG,False)
        else:
                sep = ""
        return "^fg(#" + hex_code + ") " + s + "^bg()"+sep

def get_color(nr,start,end):
        if end == start or nr >= end:
                return hex(GREEN)
        elif nr <= 0:
                return hex(RED)
        else:
                r,g,b = 0,0,0
                interval = 256 + 256
                custom_interval = abs(start-end)
                div = float(interval)/float(custom_interval)
                if div >= interval:
                        error("Interval for coloring too small, using default")
                        return WHITE
                nr = nr*div
                if custom_interval > interval:
                        custom_interval = interval
                if nr >= 256:
                        g = 0xFF
                        r = int(abs(nr - (256+256))) #counts down reverse to nr
                        ## 
                        if r == 0x100:
                                r = 0xFF
                        b = 0
                elif nr >= 0:
                        g = int(nr)
                        r = 0xFF
                        b = 0
                else:
                        error("Negative interval value???")
                        return(WHITE)
                r = r << 16
                g = g << 8
                tmp_col = r + g + b 
                if tmp_col > 0xFFFF00:
                        error("color value too high")
                return hex(tmp_col)
