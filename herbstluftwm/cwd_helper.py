#!/usr/bin/python3

import subprocess
import datetime
import sys
import os
import shlex
import psutil

def error(s):
        with open("herbstlog",'a') as f:
                time = str(datetime.datetime.now().time())[:-7] #cut seconds at the end
                f.write(time + "ERROR" + os.path.basename(__file__) + s)

out = subprocess.check_output(['xdpyinfo']).decode().split('\n')

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
out = subprocess.check_output(shlex.split('xprop -id '+hex(window))).decode().split('\n')
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

process = psutil.Process(pid)
for p in process.children(): #recursive=false
        if p.name()=='zsh' or p.name()=='bash':
                subprocess.Popen(shlex.split('urxvt -cd ' + p.cwd()))
                break
sys.exit()
