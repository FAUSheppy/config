#!/usr/bin/env bash

#######################################################################################
########################### CONSTANTS AND SHORTCUTS ###################################
#######################################################################################

hc() { "${herbstclient_command[@]:-herbstclient}" "$@" ;}
monitor=${1:-0}
geometry=( $(herbstclient monitor_rect "$monitor") )
x=${geometry[0]}
y=${geometry[1]}
panel_width=${geometry[2]}
panel_height=16
font="-*-fixed-medium-*-*-*-12-*-*-*-*-*-*-*"
bgcolor=$(hc get frame_border_normal_color)
selbg=$(hc get window_border_active_color)
selfg='#101010'
bordercolor="#26221C"
separator="^bg()^fg($selbg)|"
visible=true
date=""
pystat=
windowtitle=""


#######################################################################################
############################# BASIC SANITY CHECKS #####################################
#######################################################################################

if [ -z "$geometry" ] ;then
    echo "Invalid monitor $monitor"
    exit 1
fi
if which textwidth &> /dev/null ; then
    textwidth="textwidth";
elif which dzen2-textwidth &> /dev/null ; then
    textwidth="dzen2-textwidth";
else
    echo "This script requires the textwidth tool of the dzen2 project."
    exit 1
fi
if dzen2 -v 2>&1 | head -n 1 | grep -q '^dzen-\([^,]*-svn\|\),'; then
    dzen2_svn="true"
else
    dzen2_svn=""
fi
if awk -Wv 2>/dev/null | head -1 | grep -q '^mawk'; then
    uniq_linebuffered() {
      awk -W interactive '$0 != l { print ; l=$0 ; fflush(); }' "$@"
    }
else
    uniq_linebuffered() {
      awk '$0 != l { print ; l=$0 ; fflush(); }' "$@"
    }
fi

#######################################################################################
############################# EVENT LOOP/INPUT ########################################
#######################################################################################


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

} 2> /dev/null | {


#######################################################################################
################################## TAGS  ##############################################
#######################################################################################

    ### GET AND PARSE OUTPUT FOR TAGS FROM HERBSTCLIENT ###

    IFS=$'\t' read -ra tags <<< "$(hc tag_status $monitor)"
    while true ; do
        for i in "${tags[@]}" ; do
            case ${i:0:1} in
                '#')
                    echo -n "^bg($selbg)^fg($selfg)"
                    ;;
                '+')
                    echo -n "^bg(#9CA668)^fg(#141414)"
                    ;;
                ':')
                    echo -n "^bg()^fg(#ffffff)"
                    ;;
                '!')
                    echo -n "^bg(#FF0675)^fg(#141414)"
                    ;;
                *)
                    echo -n "^bg()^fg(#ababab)"
                    ;;
            esac
            
            ### MAKE TAGS CLICKABLE IF DZEN  VERSION SUPPORTS IT ##
            if [ ! -z "$dzen2_svn" ] ; then
                echo -n "^ca(1,\"${herbstclient_command[@]:-herbstclient}\" "
                echo -n "focus_monitor \"$monitor\" && "
                echo -n "\"${herbstclient_command[@]:-herbstclient}\" "
                echo -n "use \"${i:1}\") ${i:1} ^ca()"
            else
                echo -n " ${i:1} "
            fi
        done
        echo -n "$separator"
        echo -n "^bg()^fg() ${windowtitle//^/^^}"
        
        ### PADDING FOR PANEL TEXT ###

        right="${pystat}"
        right_text_only=$(echo -n "$right" | sed 's.\^[^(]*([^)]*)..g')
        width=$($textwidth "$font" "$right_text_only         ")
        echo -n "^pa($(($panel_width - $width)))$right"
        echo

        ### WAIT FOR INPUT DATA FROM EVENT LOOP ###

        IFS=$'\t' read -ra cmd || break
        # find out event origin
        case "${cmd[0]}" in
            tag*)
                #echo "resetting tags" >&2
                IFS=$'\t' read -ra tags <<< "$(hc tag_status $monitor)"
                ;;
            pystat)
                pystat="${cmd[@]:1}"
                ;;
            date)
                echo "resetting date" >&2
                date="${cmd[@]:1}"
                ;;
            quit_panel)
                exit
                ;;
            togglehidepanel)
                currentmonidx=$(hc list_monitors | sed -n '/\[FOCUS\]$/s/:.*//p')
                if [ "${cmd[1]}" -ne "$monitor" ] ; then
                    continue
                fi
                if [ "${cmd[1]}" = "current" ] && [ "$currentmonidx" -ne "$monitor" ] ; then
                    continue
                fi
                echo "^togglehide()"
                if $visible ; then
                    visible=false
                    hc pad $monitor 0
                else
                    visible=true
                    hc pad $monitor $panel_height
                fi
                ;;
            reload)
                exit
                ;;
            focus_changed|window_title_changed)
                windowtitle="${cmd[@]:2}"
                ;;
        esac
    done

#######################################################################################
############################ PIPE ALL THAT SHIT TO DZEN  ##############################
#######################################################################################

} 2> /dev/null | dzen2 -w $panel_width -x $x -y $y -fn "$font" -h $panel_height \
    -e 'button3=;button4=exec:herbstclient use_index -1;button5=exec:herbstclient use_index +1' \
    -ta l -bg "$bgcolor" -fg '#efefef'
