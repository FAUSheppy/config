#!/usr/bin/python3
import os
import sys
import time
from hl_utils import error, is_cip, shexec, color_remove

#Druckerguthaben
if is_cip():
        while(True):
                out = color_remove(shexec("pr_acct").split("\n")[0]).split(' ')[-1]
                with open("pracct.log",'w') as f :
                        f.write(out)
                time.sleep(60)
sys.exit()
