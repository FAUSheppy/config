#!/bin/zsh

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
if [[ $(whoami) == "root" ]]; then
    USER_COLOR="red"
    HOST_COLOR="red"
    SEPERATOR_LINE_COLOR="red"
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
if [[ $USER == 'sheppy' || $USER == 'root' ]]; then
    USER_NAME=""
    USER_HOST_SEPERATOR=""
fi

## build the complete promt ##
PS1="${SEPERATOR_LINE}${USER_NAME}${USER_HOST_SEPERATOR}${HOSTNAME}${HOST_PATH_SEPERATOR}${PATH_STR}${VERSION_CONTROL_PROMT}${PATH_INPUT_SEPERATOR}"

export GPG_TTY=$(tty)

## replace the magic values, i.e. %m with hostname ##
setopt promptsubst #enable the promt

## chromium and bash don't like LD_PRELOAD ##
alias chromium="export TMP_PRELD=$LD_PRELOAD && unset LD_PRELOAD && chromium && export LD_PRELOAD=$TMP_PRELD" 
alias bash="export TMP_PRELD=$LD_PRELOAD && unset LD_PRELOAD && bash && export LD_PRELOAD=$TMP_PRELD"

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

    if [[ "$TERM_PROGRAM" == "tmux" ]] || [[ -n $TMUX ]]; then
        export TERMINFO="xterm-256color" # peco issue 554
        export TERM="xterm-256color"
    fi
fi

## Start thunderbird with correct time-format ##
alias thunderbird="LC_ALL=en_DK.utf8 && export LC_ALL && thunderbird"

## DIRECT TO CONFIG ##
alias hlconf="vim ~/.config/herbstluftwm/autostart"
alias zshconf="vim ~/.zshrc"
alias vimconf="vim ~/.vimrc"
alias sshconf="vim ~/.ssh/config"

## /dev/zsh/random ##
alias hq="ssh -4 root@atlantishq.de"
alias hqk="ssh -4 root@katzencluster.atlantishq.de"
alias ths="ssh root@ths.atlantishq.de"

alias pcolor='for i in {0..255} ; do printf "\x1b[38;5;${i}mcolour${i} "; if [[ $(((($i+3)/6)*6)) -eq $(($i+3)) ]]; then echo; fi; done'
alias backlightctl="tee /sys/class/backlight/intel_backlight/brightness <<< $1"

## PACKAGE MANAGEMENT ##
alias psearch="apt-cache search"
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

alias mark_green="printf '\033]708;green\007';"
alias mark_blue="printf '\033]708;blue\007';"
alias mark_none="printf '\033]708;black\007'"

alias gfc='git commit . -m "[git fast commit] $(date +"%d. %h %Y - %H:%M:%S")" && git push'
alias cleanhistory="awk '{if (a[$0] < NR || a[$0] == 0){a[$0]=NR}}END{for (i in a){print a[i] " " i}}' file | sort -n | cut 1"
alias connect_synology="ssh -f -o ExitOnForwardFailure=yes -i ~/.ssh/sheppy-master -L 8000:host.docker.internal:22 root@172.16.1.4 sleep 3600 && ssh cheffe@localhost -p 8000"
#alias tcpdump_http=stdbuf -oL -eL /usr/bin/tcpdump -A -s 10240 "tcp port 8000 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)" | egrep -a --line-buffered ".+(GET |HTTP\/|POST )|^[A-Za-z0-9-]+: " | perl -nle 'BEGIN{$|=1} { s/.*?(GET |HTTP\/[0-9.]* |POST )/\n$1/g; print }'
ths_ssh="ssh -f -o ExitOnForwardFailure=yes -i .ssh/sheppy-master -L 8000:host.docker.internal:22 root@172.16.1.4 sleep 3600 && ssh cheffe@localhost -p 8000"
#trap ctrl_c INT; function ctrl_c() {};
alias sss='ssh root@192.168.1.89 -t "systemctl suspend; exit"'
