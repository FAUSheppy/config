#!/usr/bin/python3
import os
import sys
import time
import sys
import subprocess
import re
import hl_utils
import signal
import socket
from hl_constants import *
from datetime import datetime

battery_average=[]
bat_prev = -1

def sigusr1_handler(signum, frame):
        save()

def sigusr2_handler(signum, frame):
        cmd="wget --timeout=3 -O- --user cip --password "+pw()+" --quiet 'https://atlantishq.de/ciplog/"+socket.gethostname()+"&inactive&"+"none'"
        try:
            hl_utils.shexec(cmd)
        except:
            pass
        cip_logins(socket.gethostname())
        sys.exit(0)

        
def quota():
        if True:
            return
        if hl_utils.is_cip():
            q=hl_utils.shexec("cip-quota")
            ciptmp="WTF"
            home="WTF"
            test = []
            print(q)
            for l in q:
                test += [l]

            try:
                    #if l.endswith("ciptmp\n"):
                    ciptmp = test[2].split("(")[1].split(")")[0]
                #elif l.endswith("ik15ydit\n"):
                    home = test[1].split("(")[1].split(")")[0]
                    #break
            except Exception:
                return

            tmp = "Quota: "+home+"/"+ciptmp
            with open(hl_utils.hlpath("quota.cip"),"w") as f:
                print(tmp)
                f.write(tmp)

            

def pw():
            pw="NOPE"
            try:
                with open(hl_utils.hlpath("password.cip",False)) as f:
                    return f.read().strip("\n")
            except:
                return ""
            

def cip_logins(ignore=""):
            MAX_LOGINS=5
            cmd="wget -q -O- --user cip --password "+pw()+" 'https://atlantishq.de:/cipactive/active_logins'"
            try:
                l=hl_utils.shexec(cmd).split("\n")
            except:
                return ""

            if len(l) > MAX_LOGINS:
                    ret = hl_utils.color_panel("Logins: "+str(len(l)),RED)
            elif len(l) <= 1:
                    ret = ""
            else:
                #color = hl_utils.get_color(len(l),0,MAX_LOGINS+3)
                #color = color[0:2]+color[4:6]+color[2:4]+color[6:8]

                ret=''
                l=sorted(l)
                for line in l:
                    if line =='' or line==ignore:
                            continue
                    ret = ret + line + ", "
                ret = ret[:-len(", ")]
                ret = hl_utils.color_panel("Logins: "+ret,GREEN)
            with open(hl_utils.hlpath(LOGINS_LOG),'w') as f:
                f.write(ret)

def battery():
            try:
                    ## query battery ##
                    bat = hl_utils.shexec("acpi -b")
                    if bat == '':
                            return hl_utils.color_panel("Cannot query battery status",RED)
                    bat = re.compile(r'Battery [0-9]+: ').sub('',bat)
                    plain = int(bat.split('%')[0][-3:].rstrip('%').lstrip(','))
                    
                    ## imediatelly return if full and on supply ##
                    if "not charging" in bat.lower():
                            return hl_utils.color_panel(bat, GREEN)
                    if bat.startswith("Full") or bat.startswith('Unknown') or "100%" in bat or "99%" in bat:
                            return hl_utils.color_panel("On Supply and fully charged", GREEN)
                        
                    ## calculate average time remaining ##
                    sph = 60*60
                    spm = 60

                    cur_time = bat.split('%, ')[1].split(' ')[0].split(':')
                    cur = 0
                    try:
                        cur = int(cur_time[0]) * sph + int(cur_time[1]) * spm + int(cur_time[2])
                    except ValueError:
                        pass
                    
                    global battery_average
                    global bat_prev
                    battery_average += [int(cur)]
                    if len(battery_average) == 0:
                            bat_avg = "unkown"
                    else:
                            bat_avg=int(sum(battery_average) / float(len(battery_average)))

                    if len(battery_average) > 100:
                        battery_average = battery_average[:-100]
                    
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
                out = hl_utils.color_remove(hl_utils.shexec("pr_acct").split("\n")[0]).split(' ')[-1]
                with open(hl_utils.hlpath(PRINT_LOG),'w') as f:
                        f.write(out)

def bc_words():
        try:
            tmp = len(hl_utils.shexec("pdftotext {} -".format(\
                        hl_utils.hlpath(".bcpdf",use_hostname=False))).split(" "))
            with open(hl_utils.hlpath(BC_WORD_LOG),'w') as g:
                g.write(str(tmp))
        except subprocess.CalledProcessError:
            pass


def vpn_status():
    try:
        if not hl_utils.is_cip():
                out_vpn = hl_utils.shexec("ip r g 8.8.8.8").split("\n")[0]
                if "dev athq_tun" in out_vpn:
                        out_vpn = hl_utils.color_panel("VPN: In Use",GREEN)
                else:
                        out_vpn = hl_utils.color_panel("VPN: Link Down",RED)
                with open(hl_utils.hlpath(VPN_LOG),'w') as g:
                        g.write(out_vpn)
    except Exception:
        pass

def battery_status():
        if hl_utils.is_laptop():
                stat = battery()
                with open(hl_utils.hlpath(BATTERY_LOG),'w') as g:
                        g.write(stat)

last_ip="LOL"
def ip_status():
    global last_ip
    try:
        ip="Public IP: "+ hl_utils.shexec("wget -4 --no-proxy --timeout=3 -O- --quiet https://ipcheck.atlantishq.de:10443")
        if last_ip == ip:
                return
        else:
                last_ip = ip
        tmp = hl_utils.color_panel(ip,GREEN)
    except:
        last_ip = ""
        try:
            hl_utils.shexec("wget --timeout=2 -O- --quiet https://wwwcip.cs.fau.de/")
            tmp = hl_utils.color_panel("Online (ipcheck unreachable)",GREEN)
        except:
            tmp = hl_utils.color_panel("No Internet Connection",RED)
    with open(hl_utils.hlpath(IP_LOG),'w') as g:
            g.write(tmp)

def save():
            quota()
            vpn_status()
            pr_acct_status()
            battery_status()
            ip_status()
            #cip_logins()
            trace_login()

def trace_login():
        if hl_utils.is_cip():
                try:
                    tmp = hl_utils.shexec("wget --timeout=3 -O- --user cip --password "+pw()+" --quiet 'https://atlantishq.de/ciplog/"+socket.gethostname()+"&active&"+str(datetime.now())+"'")
                except:
                    tmp = "Service Unreachable"
                with open(hl_utils.hlpath("cip_logins.log"),'w') as f:
                        f.write(tmp)

if __name__ == '__main__':
        signal.signal(signal.SIGUSR1,sigusr1_handler)
        signal.signal(signal.SIGUSR2,sigusr2_handler)
        signal.siginterrupt(signal.SIGUSR1, True)
        while(True):
                save()
                if sys.argv[-1] in ['--refresh','-r']:
                        break
                time.sleep(10)
