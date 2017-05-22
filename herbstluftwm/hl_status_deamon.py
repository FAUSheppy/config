#!/usr/bin/python3
import os
import sys
import time
import subprocess
from hl_panel_content import color_panel
from hl_utils import error, is_cip, shexec, color_remove, hlpath

RED = 0xff0000
GREEN = 0x32CD32
YELLOW = 0xffff00

#Druckerguthaben
def pr_acct_status()_
        if is_cip():
                path = hlpath("pracct.log")
                out = color_remove(shexec("pr_acct").split("\n")[0]).split(' ')[-1]
                with open(path,'w+') as f:
                        f.write(out)
def vpn_status():
        if not is_cip():
                vpn_path = hlpath("vpn_status.log")
                out_vpn = subprocess.check_output(["ps","-ef"]).decode().split('\n')
                #filter(lambda x: not 'openvpn' in x,out_vpn)
                ret = 0
                for l in out_vpn:
                        if 'openvpn' in l:
                                ret += 1;
                print(ret)
                if ret <= 1:
                        out_vpn = color_panel("VPN: Link Down",RED)
                elif ret <= 3:
                        out_vpn = color_panel("VPN: In Use",GREEN)
                elif ret >= 4:
                        out_vpn = color_panel("multiple VPNs connected",YELLOW)
                else:
                        out_vpn = color_panel("VPN: WTF alles kaputt",RED)
                #print(out_vpn)
                with open(vpn_path,'w+') as g:
                        g.write(out_vpn)
                time.sleep(30)

if __name__ = '__main__':
        while(True):
                vpn_status()
                pr_acct_status()
