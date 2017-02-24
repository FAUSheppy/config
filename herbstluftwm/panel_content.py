#!/usr/bin/python3

import hl_utils

sep = " | "

RED = 0xff0000
GREEN = 0x32CD32
GREY = 0x909090
WHITE = 0xefefef
DEFAULT_FG = 0x476243 
COLOR_BORDER = 5.0

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
        if end == start or nr > end:
                return hex(GREEN)
        else:
                r,g,b = 0,0,0
                interval = 256 + 256
                custom_interval = abs(start-end)
                div = float(interval)/float(custom_interval)
                if div >= interval/3:
                        error("Interval for coloring too small, using default")
                        return WHITE
                nr = nr*div
                if custom_interval > interval:
                        custom_interval = interval
                if nr > 256:
                        g = 0xFF
                        r = int(abs(nr - (256+256))) #counts down reverse to nr
                        b = 0
                elif nr > 0:
                        g = int(nr - 256)
                        r = 0xFF
                        b = 0
                else:
                        error("Negative interval value???")
                r = r << 16
                g = g << 8
                tmp_col = r + g + b 
                if tmp_col > 0xFFFF00:
                        error("color value too high")
                return hex(tmp_col)


def guthaben():
        if hl_utils.is_cip():
                tmp = -1
                with open(hl_utils.hlpath("pracct.log")) as f:
                        tmp = float(f.read());
                guthaben = "Druckerguthaben: " + str(tmp) + " Euro"
                col = get_color(tmp,0,COLOR_BORDER)
                guthaben = color_panel(guthaben,col)
        return guthaben;

def battery():
        if hl_utils.is_laptop():
                try:
                        return color_panel(hl_utils.shexec("acpi -b | sed -r 's/Battery [0-9]+: //"),RED)
                except(ValueError):
                        return color_panel("acpi or sed not in path",RED)
        else:
                return ""

def irc():
                try:
                        fname = hl_utils.hlpath("irc.log")
                        tmp = "error"
                        with open(fname) as f:
                                pass
                        #handle pipe
                        return color_panel(PM,RED)
                except(IOError):
                        return ""
print(guthaben(),battery())
