#!/usr/bin/python3
import os
import sys
import time
import sys
import subprocess
import re
import hl_utils
import signal
from hl_constants import *

battery_average=[]
bat_prev = -1

def sigusr1_handler(signum, frame):
        save()
            

def cip_logins():
            l=hl_utils.shexec("wget -q -O- --user cip --password $(cat $HOME/.config/password.cip) 'https://atlantishq.de/cipactive/active_logins'")
            if len(l) > 5:
                    return hl_utils.color_panel("CIP Logins: "+str(len(l)),RED)
            color = hl_utils.get_color(

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
                    sph = 60*60
                    spm = 60

                    cur_time = bat.split('%, ')[1].split(' ')[0].split(':')
                    cur = int(cur_time[0]) * sph + int(cur_time[1]) * spm + int(cur_time[2])
                    
                    global battery_average
                    global bat_prev
                    battery_average += [int(cur)]
                    if len(battery_average) == 0:
                            bat_avg = "unkown"
                    else:
                            bat_avg=int(sum(battery_average) / float(len(battery_average)))
                    
                    ## keep max 10 items in queue ##
                    if len(battery_average) > VALUES_KEPT:
                        battery_average = battery_average[1:] 

                    ## color fine tuning ##
                    if plain > 10:
                            plain += BAT_COLOR_OFFSET

                    ## build string ##
                    color=hl_utils.get_color(plain,0,100)
                    tmp=hl_utils.color_panel(bat.lstrip("Charging ,").lstrip("Discharging ,").split(",")[0],color,False)

                    dez_count = 2
                    avg_h = str(int(bat_avg/sph)).zfill(dez_count)
                    avg_m = str(int((bat_avg%sph)/spm)).zfill(dez_count)
                    avg_s = str(int(bat_avg%spm)).zfill(dez_count)

                    #print(cur_time)
                    #print(bat_avg,avg_h,avg_m,avg_s)
                    #print(battery_average)
                    
                    ## prevent "flickering"
                    if(abs(int(avg_m))-abs(int(bat_prev))<5 and int(avg_h) >= 1):
                            avg_m = bat_prev
                    else:
                            bat_prev = avg_m

                    bat_str = "{}:{}:{}".format(avg_h,avg_m,"00")
                    bat_avg=hl_utils.color_panel(bat_str,color,False)


                    ## conditional coloring  ##
                    if bat.startswith("Charging"):
                            stat  = hl_utils.color_panel("Charging, ",GREEN,False) + str(tmp) + str(bat_avg)
                            stat += hl_utils.color_panel("until charged",color,True)
                    elif plain <= BATTERY_CRITICAL:
                            stat = hl_utils.color_panel(BAT_WARNING_STR,RED)
                    elif bat.startswith("Discharging"):
                            stat  = hl_utils.color_panel("Discharging, ",RED,False) + str(tmp) + str(bat_avg)
                            stat += hl_utils.color_panel("remaining",color,True)
                    else:
                            stat = hl_utils.color_panel(bat.strip('\n'),hl_utils.get_color(plain,0,100))
                    return stat
            except ValueError as e:
                    return hl_utils.color_panel(str(e),RED)

def pr_acct_status():
        if hl_utils.is_cip():
                out = hl_utils.color_remove(hl_utils.shexec(PRINT_LOG).split("\n")[0]).split(' ')[-1]
                with open(hl_utils.hlpath(PRINT_LOG),'w+') as f:
                        f.write(out)

def vpn_status():
        if not hl_utils.is_cip():
                out_vpn = hl_utils.shexec("ps -ef").split("\n")
                
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
                        out_vpn = hl_utils.color_panel("VPN: STATUS UNKOWN ??",RED)

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
                tmp = hl_utils.color_panel(p+hl_utils.shexec("wget --timeout=3 -O- --quiet https://atlantishq.de/ipcheck"),GREEN)
            except:
                tmp = hl_utils.color_panel("Offline",RED)
            g.write(tmp)

def save():
            vpn_status()
            pr_acct_status()
            battery_status()
            ip_status()

def trace_login():
        if is_cip():
                try:
                    tmp = shexec("wget --timeout=3 -O- --quiet 'https://atlantishq.de/ciplog/"+socket.gethostname()+"&active&"+str(datetime.now())+"'")
                except:
                    tmp = "Service Unreachable"
                with open(hlpath("cip_logins.log"),'w') as f:
                        f.write(tmp)

if __name__ == '__main__':
        signal.signal(signal.SIGUSR1,sigusr1_handler)
        signal.siginterrupt(signal.SIGUSR1, True)
        while(True):
                if sys.argv[-1] in ['--refresh','-r']:
                        break
                save()
                time.sleep(10)
