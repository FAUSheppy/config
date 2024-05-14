import subprocess
import datetime
import sys
import shlex
import psutil

WHITESPACE = " "
NEWLINE = "\n"
CONSOLE_TYPE = "urxvt"
HEX_BASE = 16

def get_focused_window():
    '''Ask the X-Server for the window with focus'''

    xdpyinfo = subprocess.check_output('xdpyinfo', universal_newlines=True)

    for line in xdpyinfo.split(NEWLINE):
        print(line)
        if line.startswith("focus:"):
            print("focus")

            # this line will look something like 'focus:  window 0x2200009, revert to PointerRoot' #
            window_id = 0
            for field in line.split(WHITESPACE):
                if field.startswith("0x"):
                    window_id = int(field.rstrip(","), HEX_BASE)
                    break
            
            if window_id <= 0:
                print("No Valid Focused Window Found", file=sys.stderr)
                sys.exit(1)

            return window_id

    print("No focus line found in xdpyinfo", file=sys.stderr)
    sys.exit(1)

def get_window_console_pid(window_id):
    '''Retrive the PID for a given window_id if the windows contains a console'''

    x_properties = subprocess.check_output(['xprop','-id', hex(window_id)], universal_newlines=True)
    
    selected = None
    pid = -1

    for line in x_properties.split(NEWLINE):

        if line.startswith("WM_CLASS(STRING)") and CONSOLE_TYPE in line:
            # looks like this: WM_CLASS(STRING) = "urxvt", "URxvt #
            selected = line

        if line.startswith('_NET_WM_PID(CARDINAL)'):
            # looks like this: _NET_WM_PID(CARDINAL) = 91129 #
            pid = int(line.split(" = ")[-1])

    
    if not selected or pid <= 0:
        print(f"Window does not exist or does not container f{CONSOLE_TYPE}", file=sys.stderr)
        sys.exit(1)

    return pid

def get_path_for_console_pid(pid):
    '''Retrieve the currently open path for a given console'''

    process = psutil.Process(pid)
    for p in process.children(): #recursive=false
        if p.name() in ['zsh','bash']:
            return p.cwd()


if __name__ == "__main__":
    
    window_id = get_focused_window()
    pid = get_window_console_pid(window_id)
    path = get_path_for_console_pid(pid)
    
    # run the new urxvt #
    subprocess.Popen(["urxvt", "-cd", path])
