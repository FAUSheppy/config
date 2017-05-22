#!/usr/bin/python3

import subprocess
import datetime
import sys
import os
import shlex
import psutil
from hl_utils import error, shexec

out = shexec('xdpyinfo').split('\n')

############ GET FOCUSED WINDOW ID ##############
window = -1
for l in out:
        if l.startswith('focus:'):
                for field in l.split(' '):
                        field = field.rstrip(',')
                        if(field.startswith('0x')):
                                window = int(field,16)
                if window == -1:
                        error("Failed to get window_focus\n")
if window==-1:
        sys.exit() 

############ IF URXVT GET PID ###########
pid = -1
out = subprocess.check_output(['xprop','-id',hex(window)]).decode().split('\n')
#out = shexec('xprop -id '+hex(window)).split('\n') #not working
for l in out:
        if l.startswith('WM_CLASS(STRING)') and 'urxvt' in l:
                break;
else:
        sys.exit();

for l in out:
        if l.startswith('_NET_WM_PID(CARDINAL)'):
                pid = int(l.split(' ')[-1])
if pid==-1:
        error("Failed to get PID")

############ START NEW TERMINAL ############
process = psutil.Process(pid)
for p in process.children(): #recursive=false
        if p.name() in ['zsh','bash']:
                subprocess.Popen(shlex.split('urxvt -cd ' + p.cwd()))
                break
sys.exit()
