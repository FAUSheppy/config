#!/usr/bin/python3
import os
import sys
import time
from hl_utils import error, is_cip, shexec, color_remove, hlpath

#Druckerguthaben
if is_cip():
        while(True):
                path = hlpath("pracct.log")
                out = color_remove(shexec("pr_acct").split("\n")[0]).split(' ')[-1]
                with open(path,'w+') as f:
                        f.write(out)
                time.sleep(30)
sys.exit()
