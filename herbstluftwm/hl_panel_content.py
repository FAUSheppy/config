#!/usr/bin/python3

import hl_utils
import string
import re

sep = " | "

RED = 0xff0000
GREEN = 0x32CD32
GREY = 0x909090
WHITE = 0xefefef
DEFAULT_FG = 0x476243 
COLOR_BORDER = 5.0
BAT_COLOR_OFFSET = 10

def color_panel(s,hex_code,seper=True):
        if type(hex_code)==int:
                hex_code = hex(hex_code)
        hex_code = hex_code.lstrip('0x')
        if seper:
            sep=color_panel('|',DEFAULT_FG,False)
        else:
                sep = ""
        return "^fg(#" + hex_code + ") " + s + "^bg()"+sep

def get_color(nr,start,end):
        if nr == 88:
                return hex(GREEN)
        elif end == start or nr >= end:
                return hex(GREEN)
        elif nr <= 0:
                return hex(RED)
        else:
                r,g,b = 0,0,0
                interval = 256 + 256
                custom_interval = abs(start-end)
                div = float(interval)/float(custom_interval)
                if div >= interval:
                        hl_utils.error("Interval for coloring too small, using default")
                        return WHITE
                nr = nr*div
                if custom_interval > interval:
                        custom_interval = interval
                if nr >= 256:
                        g = 0xFF
                        r = int(abs(nr - (256+256))) #counts down reverse to nr
                        #aaah fuck my life
                        if r == 0x100:
                                r = 0xFF
                        b = 0
                elif nr >= 0:
                        g = int(nr)
                        r = 0xFF
                        b = 0
                else:
                        hl_utils.error("Negative interval value???")
                        return(WHITE)
                r = r << 16
                g = g << 8
                tmp_col = r + g + b 
                if tmp_col > 0xFFFF00:
                        hl_utils.error("color value too high")
                return hex(tmp_col)


def guthaben():
        guthaben = ''
        if hl_utils.is_cip():
                raw = ""
                with open(hl_utils.hlpath("pracct.log")) as f:
                        raw = f.read();
                guthaben = "Druckerguthaben: " + raw + " Euro"
                col = get_color(float(raw),0,COLOR_BORDER)
                guthaben = color_panel(guthaben,col)
        return guthaben;

def vpn():
        vpn = ''
        if hl_utils.is_cip():
                return ''
        else:
                tmp = -1
                with open(hl_utils.hlpath("vpn_status.log")) as f:
                        tmp = f.read()
                        tmp = ' '+tmp
                return tmp;

def ip():
    with open(hl_utils.hlpath("ip.log")) as f:
        tmp = f.read()
        tmp = ' '+tmp
        return tmp;

def battery():
        if hl_utils.is_laptop():
                try:
                        bat = hl_utils.shexec("acpi -b")
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
        else:
                return ""
        

if __name__ == "__main__":
        print(ip(),vpn(),guthaben(),battery(),sep='')
