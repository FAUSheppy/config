#!/usr/bin/python3
import os
import sys
import time
import sys
import subprocess
import re
import hl_utils
from hl_constants import *

battery_average=[]

def battery():
            try:
                    ## query battery ##
                    bat = hl_utils.shexec("acpi -b")
                    if bat == '':
                            return hl_utils.color_panel("Cannot query battery status",RED)
                    bat = re.compile(r'Battery [0-9]+: ').sub('',bat)
                    plain = int(bat.split('%')[0][-3:].rstrip('%').lstrip(','))
                    
                    ## imediatelly return if full and on supply ##
                    if bat.startswith("Full") or bat.startswith('Unknown'):
                            return hl_utils.color_panel("On Supply and fully charged",GREEN)
                        
                    ## calculate average time remaining ##
                    cur_time = bat.split('%, ')[1].split(' ')[0].split(':')
                    cur = int(cur_time[0]) + int(cur_time[1]) * 60 + int(cur_time[2]) * 60 * 60
                    global battery_average
                    battery_average+=[int(cur)]
                    if len(battery_average) == 0:
                            bat_avg = "unkown"
                    else:
                            bat_avg=int(sum(battery_average) / float(len(battery_average)))
                    
                    ## color fine tuning ##
                    if plain > 10:
                            plain += BAT_COLOR_OFFSET

                    ## build string ##
                    tmp=hl_utils.color_panel(bat.lstrip("Charging ,").lstrip("Discharging ,").split(",")[0],hl_utils.get_color(plain,0,100),False)
                    bat_avg=hl_utils.color_panel(str(bat_avg),RED,False)

                    ## conditional coloring  ##
                    if bat.startswith("Charging"):
                            return hl_utils.color_panel("Charging, ",GREEN,False) + str(tmp) + str(bat_avg)
                    elif plain <= BATTERY_CRITICAL:
                            return hl_utils.color_panel(">>>>>>>>>>>>>>>> ------------ WARNING BATTER FAILURE IMMINENT ------------ <<<<<<<<<<<<<",RED)
                    elif bat.startswith("Discharging"):
                            return hl_utils.color_panel("Discharging, ",RED,False) + str(tmp) + str(bat_avg)
                    else:
                            return hl_utils.color_panel(bat.strip('\n'),hl_utils.get_color(plain,0,100))
            except ValueError as e:
                    return hl_utils.color_panel(str(e),RED)


def pr_acct_status():
        if hl_utils.is_cip():
                out = hl_utils.color_remove(hl_utils.shexec(PRINT_LOG).split("\n")[0]).split(' ')[-1]
                with open(hl_utils.hlpath(PRINT_LOG),'w+') as f:
                        f.write(out)

def vpn_status():
        if not hl_utils.is_cip():
                out_vpn = hl_utils.shexec("ps -ef")
                #out_vpn = subprocess.check_output(["ps","-ef"]).decode().split('\n')
                
                ret = 0 
                for l in out_vpn:
                        if 'openvpn' in l and not 'sudo' in l and not 'grep' in l and not 'cip.sh' in l:
                                ret += 1;

                if ret == 0:
                        out_vpn = hl_utils.color_panel("VPN: Link Down",RED)
                elif ret == 1:
                        out_vpn = hl_utils.color_panel("VPN: In Use",GREEN)
                elif ret > 1:
                        out_vpn = hl_utils.color_panel("multiple VPNs connected",YELLOW)
                else:
                        out_vpn = hl_utils.color_panel("VPN: ret was "+str(ret)+" ??",RED)

                with open(hl_utils.hlpath(VPN_LOG),'w+') as g:
                        g.write(out_vpn)

def battery_status():
        if hl_utils.is_laptop():
                with open(hl_utils.hlpath(BATTERY_LOG),'w') as g:
                        g.write(battery())

def ip_status():
    with open(hl_utils.hlpath(IP_LOG),'w') as g:
            p="Public IP: "
            try:
                tmp=hl_utils.color_panel(p+hl_utils.shexec("wget --timeout=3 -O- --quiet https://atlantishq.de/ipcheck"),GREEN)
            except:
                tmp=hl_utils.color_panel("Offline",RED)
            g.write(tmp)


if __name__ == '__main__':
        while(True):
                vpn_status()
                pr_acct_status()
                battery_status()
                ip_status()
                if sys.argv[-1]=='--refresh':
                        break
                time.sleep(5)
