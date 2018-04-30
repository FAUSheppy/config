#!/usr/bin/python3
import hl_utils
from hl_constants import *
import string
import re
from datetime import datetime

def guthaben():
        guthaben = ''
        if hl_utils.is_cip():
                raw = ""
                with open(hl_utils.hlpath(PRINT_LOG)) as f:
                        raw = f.read();
                guthaben = "Druckerguthaben: " + raw + " Euro"
                col = hl_utils.get_color(float(raw),0,COLOR_BORDER)
                guthaben = hl_utils.color_panel(guthaben,col)
        return guthaben;

def vpn():
        vpn = ''
        if hl_utils.is_cip():
                return ''
        else:
                with open(hl_utils.hlpath(VPN_LOG)) as f:
                        tmp = f.read()
                        tmp = ' '+tmp
                        return tmp;

def ip():
    with open(hl_utils.hlpath(IP_LOG)) as f:
        tmp = f.read()
        tmp = ' '+tmp
        return tmp;

def battery():
        if hl_utils.is_laptop():
            try:
                with open(hl_utils.hlpath(BATTERY_LOG)) as f:
                    tmp = f.read()
                    tmp = ' '+tmp
                    return tmp;
            except Exception as e:
                return color_panel(str(e),RED)
        else:
                return ""
        
def date():
        return hl_utils.shexec("date +' ^fg(#efefef)%H:%M^fg(#909090), %Y-%m-^fg(#efefef)%d'")

def logins():
        try:
            with open(hl_utils.hlpath(LOGINS_LOG),'r') as f:
                    return f.read()
        except:
                return ""

def countdown():
        delta = datetime(year=2018,month=7,day=22,hour=20) - datetime.now()
        if delta.days > 1:
            tmp = "{} von 180 Tagen bis Abgabe verbleibend".format(delta.days)
        else:
            tmp = "{}h bis BC Abgabe".format(delta.hours)
        tmp = hl_utils.color_panel(tmp,YELLOW)
        return tmp


if __name__ == "__main__":
        print(countdown(),logins(),ip(),vpn(),guthaben(),battery(),date(),sep='',end='')
