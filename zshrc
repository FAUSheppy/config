#### ZSH-INTERNAL ####
### HISTORY ###
STSIZE=2000
SAVEHIST=2000
HISTFILE=~/.config/zshhistory.log

### COLOR STDERR ###
#legacy, this causes problems in output odering exec 2>>( while IFS='' read X; do print "\e[91m${X}\e[0m" > /dev/tty; done & )
LD_PRELOAD="$HOME/.config/libcoloredstderr.so"
COLORED_STDERR_FDS=2,
export LD_PRELOAD COLORED_STDERR_FDS

### PROMT ###
MAIN_PROMT_COLOR="green"
USER_COLOR="yellow"
if [[ $USER == "root" ]]; then
    USER_COLOR="red"
    MAIN_PROMT_COLOR="red"
fi
setopt promptsubst
CMD_START=$'%F{$MAIN_PROMT_COLOR}--->%f '
PS1=$'%F{$USER_COLOR}%m%f%F{red}:%f%F{cyan}%~%f\n'$CMD_START #promt
PS1=%F{$MAIN_PROMT_COLOR}$'${(r:$COLUMNS::\u2500:)}'%f$PS1

### STYLE ###
zstyle ':completion:*:default' list-prompt '%p'
zstyle ':completion:*' use-cache yes; zstyle ':completion:*' cache-path #~/.zsh/cache (~/.zsh muss existieren)
zstyle ':completion:::::' completer  _expand _complete _prefix _ignored _approximate # _expand expandiert dinge wie $FOO<Tab>, _complete ist
#das normale completion, _prefix ignoriert alles nach dem Cursor (für complete_in_word) _ignored ignoriered gewisse matches, ist mit
#_approximate wichtig, damit nicht falsche dinge completet werden, _approximate sucht nach ähnlichen Dingen
zstyle -e ':completion:*:approximate:*' max-errors 'reply=( $(( ($#PREFIX + $#SUFFIX) / 5 )) )' # maximal alle 3 zeichen ein fehler
zstyle ':completion:*:(^approximate):*' matcher-list 'm:{a-z}={A-Z}' # Kleinschreibung automatisch zu Großschreibung korrigieren.
zstyle ':completion:*:expand:*' keep-prefix yes #halt praefix behalten, HOME nicht zu cip/home blablabla expandierekn
zstyle ':completion:*' list-suffixes yes # completet a/b/c<tab> zu abc/bcd/coo
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS} # dircolors für completion
zstyle ':completion:*' menu select

### OPTIONS ###
setopt noclobber #keine datein ueberscheiben mit >
setopt appendhistory; setopt incappendhistory # history immer sofort
setopt histignoredups #keine duplikate
setopt histignorespace #keine dinge mit leerzeichen in history
setopt nolistambiguous # sofort alle Möglichkeiten anzeigen
setopt completeinword # in Wörtern completen, braucht der _prefix completer

### GENERAL ###
bindkey '^R' history-incremental-pattern-search-backward
zmodload zsh/complist #bessere listen
autoload -Uz compinit; compinit #completioni

### UMASK ###
umask 077

#### ZSH ALIASES ####
## BASIC ##
alias -g E='2>&1'
alias -g N='>/dev/null'
alias -g EN='2>/dev/null'
alias -g L='2>&1 | less'
alias -g G='| grep'
alias -g S='| sort'
alias -g ...='../..'
alias -g D='| dot -Tpng >'
alias mv='mv -i'
alias cp='cp -i'
alias ..='cd ..'

## Anti-LD-Preload Chromium Wrapper ##
alias chromium="export TMP_PRELD=$LD_PRELOAD && /bin/bash -c 'unset LD_PRELOAD && chromium' && export LD_PRELOAD=$TMP_PRELD"

## LOCKS ##
if [[ $HOST =~ atlantis* ]]; then
    alias i3lock="i3lock --image=/home/ik15ydit/.config/i3lock/bg.png"
    alias hlock="i3lock --image=/home/ik15ydit/.config/i3lock/bg.png -t"
else
    alias transparent_xlock="xlock -mode blank -geometry 1x1"
fi

## PACKAGE MANAGEMENT ##
alias psearch="apt-cache search"

## GENERAL SHORTCUTS ##
if [[ $HOST =~ atlantis* ]]; then
    #alias gedit="gedit 2&>/dev/null &"
    alias kpaint="kolourpaint 2&>/dev/null &"
    alias telegram='ssh uni -t "/proj/ciptmp/ik15ydit/Zeug/Telegram/tg/bin/telegram-cli -k tg-server.pub"'
    alias telegram-plain='ssh uni -t "/proj/ciptmp/ik15ydit/Zeug/Telegram/tg/bin/telegram-cli --disable-colors --disable-readline -k tg-server.pub"'

    alias x='startx'
else
    alias pcolor='for i in {0..255} ; do printf "\x1b[38;5;${i}mcolour${i} "; if [[ $(((($i+3)/6)*6)) -eq $(($i+3)) ]]; then echo; fi; done'
    alias telegram='/proj/ciptmp/ik15ydit/Zeug/Telegram/tg/bin/telegram-cli -k tg-server.pub'
fi
alias "ipconf"="ip addr show"

## General ##
if [[ $HOST =~ atlantis* ]]; then
    alias -g jpg2png="echo 'use convert [file_in.jpg] [file_out.png]'" 
    alias mpc-curses='ncmpc --host 10.100.4.22'
    alias wgplayer='ncmpc --host 10.100.4.22'
fi

## Pathing ##
CIP_MOUNTPOINT="$HOME/mountpoints/cip_root"
FS_PREFIX=""
CIPTMP="/proj/ciptmp/$USER"
if [[ $HOST =~ atlantis* ]]; then
        FS_PREFIX=$CIP_MOUNTPOINT
fi
alias ct="cd $FS_PREFIX$CIPTMP"
alias mpstubs="cd $FS_PREFIX$CIPTMP/reps/mpstubs/"
alias tutoren="cd $FS_PREFIX$CIPTMP/reps/tutorenShare"
alias idb="cd $FS_PREFIX$CIPTMP/Backup/IDB_2017/"

## MARKINGBIRD ##
export PYTHONPATH=/local/python3-typing
if [[ $HOST == faui* ]]; then
    alias mabird="/proj/ciptmp/ik15ydit/reps/MarkingBird/MarkingBird.py"
fi

## PATHS ##
if [[ $HOST =~ faui* ]]; then
    export JAVA_HOME="/local/java-1.8"
fi

## CONNECT UNI ##
alias irc="ssh ircbox.cs.fau.de -t 'command; tmux a'"
alias -g uni="faui06c.cs.fau.de"
alias cipkey="ssh-add ~/.ssh/ciplogin"
alias cipra="xpra start ssh:ik15ydit@faui00n.cs.fau.de:100 --start-child urxvt"
alias mountcip="sshfs ik15ydit@faui00n.cs.fau.de:/ -o idmap=user $CIP_MOUNTPOINT"
alias umountcip="fusermount -u $CIP_MOUNTPOINT"

## DIRECT TO CONFIG ##
alias hlconf="vim ~/.config/herbstluftwm/autostart"
alias zshconf="vim ~/.zshrc"
alias vimconf="vim ~/.vimrc"
alias sshconf="vim ~/.ssh/config"

## CIP SHORTCUTS ##
if [[ $HOST =~ faui* ]]; then
    alias iceweasel="bash -c 'cp -f --recursive .mozilla/firefox/d9m0msa0.test /var/tmp && chmod 700 --recursive /var/tmp/d9m0msa0.test/ && iceweasel --profile /var/tmp/d9m0msa0.test && rm -rf /var/tmp/d9m0msa0.test'"
    alias mpstubs="cd /proj/ciptmp/ik15ydit/reps/mpstubs/"
    alias reps="cd /proj/ciptmp/ik15ydit/reps/"
    alias rudipub='cd /home/cip/2010/he29heri/pub/'
    alias sudo="echo THIS IS THE CIP NOT YOUT COMPUTER!!!!! >&2"
    alias su="echo THIS IS THE CIP NOT YOUT COMPUTER!!!!! >&2"
fi
## MOUNTABLE CIP-SHORTCUTS ##
if [[ $HOST =~ atlantis* ]]; then
    alias ciptmp="cd ~/mountpoints/cip_root/proj/ciptmp/ik15ydit/"
    alias ciphome="cd ~/mountpoints/cip_root/home/cip/2013/ik15ydit/"
fi

## DIPLAY CONTROL ##
if [[ $HOST =~ atlantis* ]]; then
    alias dual="xrandr --output DVI-I-2 --right-of DVI-I-1"
    alias shutown="/sbin/poweroff"
fi
if [[ $HOST == "atlantislaptop" ]]; then
    alias backlightctl="tee /sys/class/backlight/intel_backlight/brightness <<< $1"
    alias nodisplayoff='xset s off'
fi

## JAVA ##
alias javac-all-test4='javac -cp .:/usr/share/java/junit4.jar *.java'
alias java-test4='java -cp .:/usr/share/java/junit4.jar'

## /zsh/random ##
alias spc='gcc -std=c99 -pedantic -Wall -Werror -D_XOPEN_SOURCE=700 -o'
alias woist='ssh ircbox nc localhost 1339 | grep -B1 " in .zshrci'
alias logins='nc localhost 1339 | grep -B1'
alias cltex="rm *.log *.aux *.fdb_latexmk *.fls"
alias wordcount="find . -type f -exec cat {} + | wc -w"
alias bv="urxvt -e vim $1"
alias v="vim $1"

## LS ##
LS_COLORS=$LS_COLORS:'di=0;35:'; export LS_COLORS
alias la="ls -lAh --color=auto"
alias ll="ls -llh --color=auto"
alias ls="ls --color=auto"
alias l="ls -lh --color=auto"

## SSH-KEYS ##
gitssh=~/.ssh/gitrsa
function key(){
        eval `ssh-agent`
        ssh-add $gitssh
}

## ROOT ##
alias udev_reload="udevadm control --reload-rules && udevadm trigger" #reload all udevrules on the fly

### DISABLE MESSAGES ###
if [[ $HOST =~ faui* ]]; then
    mesg n
fi
