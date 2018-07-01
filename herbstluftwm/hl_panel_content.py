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

def quota():
        q = ''
        if not hl_utils.is_cip():
                return ''
        else:
                with open(hl_utils.hlpath("quota.cip")) as f:
                    return f.read()

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
        if len(tmp) > 20:
            tmp = hl_utils.color_panel("Public IP: IP6 ",GREEN)
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

def bcw():
        try:
            with open(hl_utils.hlpath(BC_WORD_LOG),'r') as f:
                    tmp = int(f.read())
                    string = "{} of 6000 words".format(tmp)
                    return hl_utils.color_panel(string,hl_utils.get_color(tmp,0,6000,reverse=False))
        except:
                return ""
def bwp():
        tmp = ""
        cur = 29
        try:
            with open(hl_utils.hlpath(BC_PAGE_LOG),'r') as f:
                tmp = "{} pages".format(f.read().strip())
        except:
                tmp = "{} pages".format(cur)
        tmp = hl_utils.color_panel(tmp,hl_utils.get_color(cur,0,60))
        return tmp


def countdown():
        delta = datetime(year=2018,month=7,day=23,hour=8) - datetime.now()
        if delta.days > 1:
            tmp = "{} von 150 Tagen bis Abgabe verbleibend".format(delta.days)
        else:
            tmp = "{}h bis BC Abgabe".format(delta.hours)
        tmp = hl_utils.color_panel(tmp,hl_utils.get_color(delta.days,0,180))
        return tmp


if __name__ == "__main__":
        print(bwp(),bcw(),countdown(),logins(),ip(),vpn(),guthaben(),battery(),date(),sep='',end='')
