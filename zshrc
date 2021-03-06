#!/bin/zsh
########################################################################################################
########################################### COLOR STDERR################################################
########################################################################################################

## see https://ruderich.org/simon/#coloredstderr
COLOR_STDERR=true

## disable for some hosts
if [[ $HOST == "squarez" ]]; then
    COLOR_STDERR=true
fi

if [[ $COLOR_STDERR == true ]]; then
    LD_PRELOAD="$HOME/.config/libcoloredstderr.so"
    COLORED_STDERR_FDS=2,
    export LD_PRELOAD COLORED_STDERR_FDS
fi

## this is a little hack to make zsh-error output to also appear as red
if [[ $FIRST_RUN == "FALSE" ]]; then
    ;
else
    FIRST_RUN="FALSE"
    export FIRST_RUN
    exec zsh
fi

########################################################################################################
############################################## PROMT ###################################################
########################################################################################################

## git ##
setopt prompt_subst
autoload -Uz vcs_info
zstyle ':vcs_info:*' actionformats '%F{5}[%F{2}%b%F{3}|%F{1}%a%F{5}]%f '
zstyle ':vcs_info:*' formats '%F{5}[%F{2}%b%F{5}]%f '
zstyle ':vcs_info:(sv[nk]|bzr):*' branchformat '%b%F{1}:%F{3}%r'
zstyle ':vcs_info:*' enable git cvs svn

# or use pre_cmd, see man zshcontrib
vcs_info_wrapper() {
  vcs_info
  if [ -n "$vcs_info_msg_0_" ]; then
    echo "%{$fg[grey]%}${vcs_info_msg_0_}%{$reset_color%}$del"
  fi
}
VERSION_CONTROL_PROMT=$'$(vcs_info_wrapper)'

## colors ##
SEPERATOR_LINE_COLOR="green"
USER_COLOR="yellow"
USER_HOST_SEPERATOR_COLOR="red"
HOST_COLOR="yellow"
HOST_PATH_SEPERATOR_COLOR="red"
PATH_COLOR="cyan"
PATH_INPUT_SEPERATOR_COLOR="green"

## different color for root ##
if [[ $USER == "root" ]]; then
    USER_COLOR="red"
    HOST_COLOR="red"
    SEPERATOR_LINE_COLOR="red"
fi

## different color for certain hosts ##
if [[ $HOST == "squarez" ]]; then
    USER_COLOR="cyan"
fi

## seperators ##
USER_HOST_SEPERATOR="@"
HOST_PATH_SEPERATOR=":"
PATH_INPUT_SEPERATOR="--->"
PATH_INPUT_NEWLINE=true

## build all parts ##
SEPERATOR_LINE=%F{$SEPERATOR_LINE_COLOR}$'${(r:$COLUMNS::\u2500:)}'%f
USER_NAME="%F{$USER_COLOR}%n%f"
USER_HOST_SEPERATOR="%F{$USER_HOST_SEPERATOR_COLOR}${USER_HOST_SEPERATOR}%f"
HOSTNAME="%F{$HOST_COLOR}%m%f"
HOST_PATH_SEPERATOR="%F{$HOST_PATH_SEPERATOR_COLOR}:%f"
PATH_STR="%F{$PATH_COLOR}%~%f"
PATH_INPUT_SEPERATOR="%F{$SEPERATOR_LINE_COLOR}${PATH_INPUT_SEPERATOR} %f"
if [[ $PATH_INPUT_NEWLINE == "true" ]]; then
    PATH_INPUT_SEPERATOR="
${PATH_INPUT_SEPERATOR}"
fi

## no usernames for my default accounts ##
if [[ $USER == 'sheppy' || $USER == 'ik15ydit' || $USER == 'root' ]]; then
    USER_NAME=""
    USER_HOST_SEPERATOR=""
fi

## build the complete promt ##
PS1="${SEPERATOR_LINE}${USER_NAME}${USER_HOST_SEPERATOR}${HOSTNAME}${HOST_PATH_SEPERATOR}${PATH_STR}${VERSION_CONTROL_PROMT}${PATH_INPUT_SEPERATOR}"

## replace the magic values, i.e. %m with hostname ##
setopt promptsubst #enable the promt

## chromium and bash don't like LD_PRELOAD ##
alias chromium="export TMP_PRELD=$LD_PRELOAD && unset LD_PRELOAD && chromium && export LD_PRELOAD=$TMP_PRELD" 
alias bash="export TMP_PRELD=$LD_PRELOAD && unset LD_PRELOAD && bash && export LD_PRELOAD=$TMP_PRELD"

########################################################################################################
######################################## OPTIONS #######################################################
########################################################################################################

## show list of tab-completing options
zstyle ':completion:*:default' list-prompt '%p'

## cache completion for re-use (path must exist)
zstyle ':completion:*' use-cache yes; zstyle ':completion:*' cache-path

## _complete    -> completiong
## _expand      -> expand variables
## _prefix      -> ignore everything behind cursor
## _approximate -> fuzzy completion
## _ignore      -> ignore some matches (i.e. directories when doing cd)
zstyle ':completion:::::' completer  _expand _complete _prefix _ignored _approximate

## one wrong character every X characters is corrected
## X = 5 is a reasonable default
zstyle -e ':completion:*:approximate:*' max-errors 'reply=( $(( ($#PREFIX + $#SUFFIX) / 5 )) )'

## correct lowercase to uppercase
zstyle ':completion:*:(^approximate):*' matcher-list 'm:{a-z}={A-Z}' # Kleinschreibung automatisch zu Großschreibung korrigieren.

## keep magic prefixes like '~' when expanding
zstyle ':completion:*:expand:*' keep-prefix yes #halt praefix behalten, HOME nicht zu cip/home blablabla expandierekn

## compelte a/b/c<tab> zu abc/bcd/coo
zstyle ':completion:*' list-suffixes yes

## colors in completion menu ##
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}

## allow autocomplete-navigation with arrowkeys
zstyle ':completion:*' menu select #enable a menu which can be browsed with arrow keys

## do not overwrite files with '>' "
setopt noclobber

## write command to historyfile imediatelly
setopt appendhistory; setopt incappendhistory

## max size and location of history-savefile
STSIZE=2000000
SAVEHIST=200000
HISTFILE=~/.config/zshhistory.log

## no duplicated commands
setopt histignoredups

## no emptylines
setopt histignorespace

## tab completion after pressing tab once (default is twice)
setopt nolistambiguous

## allow in word completion 
setopt completeinword

## allow ommition of cd to change directory, use with caution ##
setopt autocd

## i forgot what this does but completion doesnt work without it
autoload -Uz compinit; compinit #completioni

### UMASK ###
umask 077

## ask before overwriting files with mv/cp
alias mv='mv -i'
alias cp='cp -i'

## color scheme for LS ##
LS_COLORS=$LS_COLORS:'di=0;35:'; export LS_COLORS

## A -> show hidden files, but not . and ..
## a -> show hidden files
## l -> show additional information for files
## h -> show human readable file-size (1M instead of 1000000 bytes)
## --color=auto color output with $LS_COLORS
alias la="ls -lah --color=auto"
alias ll="ls -llh --color=auto"
alias ls="ls --color=auto"
alias l="ls -lh --color=auto"
alias ..='cd ..'
alias ...='cd ../../'

#### SEARCH HISTORYFILE ####
if ! [ -x "$(command -v peco)" ]; then
    bindkey '^R' history-incremental-pattern-search-backward
else
    ## bind peco to ctrl-R as a better reverse search than the buitin if it is availible
    reverse_search(){print -z "$(tac ${HISTFILE} | peco)"}
    zle -N rs_peco reverse_search
    bindkey ^R rs_peco
    PECO=/usr/bin/
fi

### USEFULL CIP STUFF ###

## disable messages to tty's since it's used for trolling in university way too often
if [[ $HOST =~ faui* || $HOST =~ ircbox ]]; then
    mesg n
fi

## lock screen but still let people read it
alias transparent_xlock="xlock -mode blank -geometry 1x1"


###################################################### END OF BASIC CONFIG ######################################################


## Start thunderbird with correct time-format ##
alias thunderbird="LC_ALL=en_DK.utf8 && export LC_ALL && thunderbird"

## DIRECT TO CONFIG ##
alias hlconf="vim ~/.config/herbstluftwm/autostart"
alias zshconf="vim ~/.zshrc"
alias vimconf="vim ~/.vimrc"
alias sshconf="vim ~/.ssh/config"

## GIT ##
alias gstat="git status"
alias gpull="git pull"
alias gpush="git push"
alias gcom="git commit -a"
alias gadd="git add"

## REMOTE HOSTS ##
alias -g sq="sheppy@squarez.fauiwg.de"

## PACKAGE MANAGEMENT ##
alias psearch="apt-cache search"

## Pathing ##
CIP_MOUNTPOINT="$HOME/mountpoints/cip_root"
FS_PREFIX=""
CIPTMP="/proj/ciptmp/$USER"
if [[ $HOST =~ atlantis* ]]; then
        FS_PREFIX=$CIP_MOUNTPOINT
fi
alias tutoren="cd $FS_PREFIX$CIPTMP/reps/tutorenShare"

## MARKINGBIRD ##
export PYTHONPATH=/local/python3-typing
if [[ $HOST == faui* ]]; then
    alias mabird="/proj/ciptmp/ik15ydit/reps/MarkingBird/MarkingBird.py"
fi

## CONNECT UNI ##
alias -g uni="ik15ydit@faui06c.cs.fau.de"
alias cipkey="ssh-add ~/.ssh/ciplogin"
alias cipra="xpra start ssh:ik15ydit@faui0sr0.cs.fau.de:100 --start-child urxvt"
alias mountcip="sshfs ik15ydit@faui00n.cs.fau.de:/ -o reconnect,idmap=user $CIP_MOUNTPOINT"
alias umountcip="fusermount -u $CIP_MOUNTPOINT"

## CIP SHORTCUTS ##
if [[ $HOST =~ faui* ]]; then
    alias iceweasel="bash -c 'cp -f --recursive .mozilla/firefox/d9m0msa0.test /var/tmp && chmod 700 --recursive /var/tmp/d9m0msa0.test/ && iceweasel --profile /var/tmp/d9m0msa0.test && rm -rf /var/tmp/d9m0msa0.test'"
    alias rudipub='cd /home/cip/2010/he29heri/pub/'
    alias sudo="echo THIS IS THE CIP NOT YOUR COMPUTER!!!!! >&2"
    alias su="echo THIS IS THE CIP NOT YOUR COMPUTER!!!!! >&2"
fi

## ATLANTIS* ##
if [[ $HOST =~ atlantis* ]]; then
    alias shutown="/sbin/poweroff"
    alias s2disk="sudo /usr/sbin/s2disk"
    alias -g ciptmp="~/mountpoints/cip_root/proj/ciptmp/ik15ydit/"
    alias -g ciphome="~/mountpoints/cip_root/home/cip/2013/ik15ydit/"
    alias mpc-curses='ncmpc --host 10.100.4.22'
    alias wgplayer='ncmpc --host 10.100.4.22'
fi
if [[ $HOST == "atlantislaptop" ]]; then
    alias backlightctl="tee /sys/class/backlight/intel_backlight/brightness <<< $1"
fi

## /dev/zsh/random ##
alias nodisplayoff='xset s off'
alias javac-all-test4='javac -cp .:/usr/share/java/junit4.jar *.java'
alias java-test4='java -cp .:/usr/share/java/junit4.jar'
alias cltex="rm *.log *.aux *.fdb_latexmk *.fls"
alias wordcount="find . -type f -exec cat {} + | wc -w"
alias bv="urxvt -e vim $1"
alias v="vim $1"
alias hgrep="cat ~/.config/zshhistory.log | grep"
alias hq="ssh -4 root@atlantishq.de"
alias sync-atlantishq="rsync -avz -r -P root@atlantishq.de:/home/home_backup/ /home/sheppy/archive"
alias -g public_ip='wget --timeout=3 -O- --quiet https://atlantishq.de/ipcheck'
alias gitkey="ssh-add ~/.ssh/gitrsa"
alias pcolor='for i in {0..255} ; do printf "\x1b[38;5;${i}mcolour${i} "; if [[ $(((($i+3)/6)*6)) -eq $(($i+3)) ]]; then echo; fi; done'
alias 'vpn?'='ps -ef | grep  openvpn | grep -v grep'
alias telegram='\ssh telegram-sheppy@atlantishq.de -i ~/.ssh/telegram -t "~/tg/bin/telegram-cli"'
alias x='exec startx'
alias clear_swap="echo 'This can take serveral minutes if swap was full' &&sudo swapoff -a && sudo swapon -a"
whateverprovides(){
    apt-file search --regexp "bin/$1""$"
}
export whateverprovides

### COLOR SSH ###
ssh_func(){
    printf '\033]708;red\007';
    /usr/bin/ssh $@;
    printf '\033]708;black\007';
}
alias ssh="ssh_func"

### Terminal Border-Colors ###
alias mark_green="printf '\033]708;green\007';"
alias mark_blue="printf '\033]708;blue\007';"
alias mark_none="printf '\033]708;black\007'"

## kill all cip sessions except this pc ##
logout_all(){
    TMP=$(wget -q -O- --user cip --password $(cat $HOME/.config/herbstluftwm/password.cip) "https://atlantishq.de/cipactive/active_logins")
    echo $TMP | while read line; do
            if [[ $line != $HOST ]]; then
                ssh -n -q ${line}.cs.fau.de -t "pkill --signal USR2 hl_status && pkill -u ik15ydit"
            fi
    done
}
export logout_all

### EXPERIMENTAL ###
alias insurgency_status="ssh insurgency@atlantishq.de -t /usr/local/bin/insurgency_rcon status"
alias python=python3
alias dirc="ssh sheppy@atlantishq.de -t 'command;tmux a -d'"
alias gfc='git commit . -m "[git fast commit] $(date +"%d. %h %Y - %H:%M:%S")" && git push'
alias bc="cd /proj/cipdata/ik15ydit/license-confusion-bc"
export PYTHONPATH=/home/cip/2013/ik15ydit/python-local
alias -g atip="echo 93.104.211.59"
alias atp="~/.config/playercount.py"
alias players='~/trash/test/test.py'
alias cleanhistory="awk '{if (a[$0] < NR || a[$0] == 0){a[$0]=NR}}END{for (i in a){print a[i] " " i}}' file | sort -n | cut 1"
alias ths="ssh root@ths.atlantishq.de"

# insurgency debugging
alias balance="curl localhost:5000/getbalancedteams\?players=Shepppy,OrhunReiz,Bluejalapeno4,RandomItaliano\&names=true"
alias quality="curl localhost:5000/quality\?playerswithteams=Shepppy,OrhunReiz\|Bluejalapeno4,RandomItaliano\&names=true"
