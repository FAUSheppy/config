#!/usr/bin/env bash

source uniq_linebuffered.sh

### Generates the output for the rightside of the panel ### 

hc() { "${herbstclient_command[@]:-herbstclient}" "$@" ;}

hc pad $monitor $panel_height
{
    while true ; do 
        printf 'pystat\t%s\n' "$($HOME/.config/herbstluftwm/hl_panel_content.py)"
        sleep 1 || break
    done > >(uniq_linebuffered) &

    ## save pid and wait for signal ##
    childpid=$!
    hc --idle
    kill $childpid
}
