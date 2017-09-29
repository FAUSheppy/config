#!/usr/bin/python3
import os
import sys
import time
import sys
import subprocess
from hl_panel_content import color_panel, get_color
from hl_utils import error, is_cip, shexec, color_remove, hlpath, is_laptop
import re

RED = 0xff0000
GREEN = 0x32CD32
YELLOW = 0xffff00
BAT_COLOR_OFFSET = 10 


#Druckerguthaben
def pr_acct_status():
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
                #worst case thats about 1k lines
                for l in out_vpn:
                        if 'openvpn' in l and not 'sudo' in l and not 'grep' in l and not 'cip.sh' in l:
                                ret += 1;
                #print(ret)
                if ret == 0:
                        out_vpn = color_panel("VPN: Link Down",RED)
                elif ret == 1:
                        out_vpn = color_panel("VPN: In Use",GREEN)
                elif ret > 1:
                        out_vpn = color_panel("multiple VPNs connected",YELLOW)
                else:
                        out_vpn = color_panel("VPN: ret was "+str(ret)+" ??",RED)
                #print(out_vpn)
                with open(vpn_path,'w+') as g:
                        g.write(out_vpn)

def battery():
            try:
                    bat = shexec("acpi -b")
                    if bat == '':
                            return color_panel("BATTERY FAILURE",RED)
                    bat = re.compile(r'Battery [0-9]+: ').sub('',bat)
                    plain = int(bat.split('%')[0][-3:].rstrip('%').lstrip(','))
                        
                    #cur_time = [bat.split('%, ')[1].split(' ')[0].split(':')]

                    if plain > 10:
                            plain += BAT_COLOR_OFFSET
                        
                    if bat.startswith("Charging"):
                            return color_panel("Charging",GREEN,seper=False) + color_panel(bat.lstrip("Charging ,").strip('\n'),get_color(plain,0,100))
                    elif bat.startswith("Full") or bat.startswith('Unknown'):
                            return color_panel("On Supply and fully charged",GREEN)
                    elif plain <= 1:
                            return color_panel(">>>>>>>>>>>>>>>> --------------- WARNING BATTER FAILURE IMMINENT --------------- <<<<<<<<<<<<<",RED)
                    elif bat.startswith("Discharging"):
                            return color_panel("Discharging",RED,seper=False) + color_panel(bat.lstrip("Discharging ,").strip('\n'),get_color(plain,0,100))
                    else:
                            return color_panel(bat.strip('\n'),get_color(plain,0,100))
            except ValueError as e:
                    return color_panel(str(e),RED)

def battery_status():
        if is_laptop:
                with open(hlpath("battery.log"),'w') as g:
                        g.write(battery())

def ip_status():
    with open(hlpath("ip.log"),'w') as g:
            p="Public IP: "
            try:
                tmp=color_panel(p+shexec("wget --timeout=3 -O- --quiet https://atlantishq.de/ipcheck"),GREEN)
            except:
                tmp=color_panel("Offline",RED)
            g.write(tmp)


if __name__ == '__main__':
        #print('"'+sys.argv[-1]+'"')
        while(True):
                vpn_status()
                pr_acct_status()
                battery_status()
                ip_status()
                if sys.argv[-1]=='--refresh':
                        break
                time.sleep(30)


