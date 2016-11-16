STSIZE=2000; SAVEHIST=2000; HISTFILE=~/.zsh/history #historylaenge
CMD_START=$'%F{green}--->%f '
PS1=$'%F{yellow}%m%f%F{red}:%f%F{cyan}%~%f\n'$CMD_START #promt

#coloring stderr, causes problems in output odering
#exec 2>>( while IFS='' read X; do print "\e[91m${X}\e[0m" > /dev/tty; done & )
#better by rudi_s
LD_PRELOAD='/home/ik15ydit/.config/libcoloredstderr.so'
COLORED_STDERR_FDS=2,
export LD_PRELOAD COLORED_STDERR_FDS

#markingbird
export PYTHONPATH=/local/python3-typing

#seperation string between commands
setopt promptsubst
PS1=%F{green}$'${(r:$COLUMNS::\u2500:)}'%f$PS1

zstyle ':completion:*:default' list-prompt '%p'
zmodload zsh/complist #bessere listen
autoload -Uz compinit; compinit #completioni
setopt noclobber #keine datein ueberscheiben mit >
alias mv='mv -i'
alias cp='cp -i'
setopt appendhistory; setopt incappendhistory # history immer sofort
setopt histignoredups #keine duplikate
setopt histignorespace #keine dinge mit leerzeichen in history
zstyle ':completion:*' use-cache yes; zstyle ':completion:*' cache-path #~/.zsh/cache (~/.zsh muss existieren)
#autoload -Uz colors; colors # farben in prompts und completioni
setopt nolistambiguous # sofort alle Möglichkeiten anzeigen
setopt completeinword # in Wörtern completen, braucht der _prefix completer
zstyle ':completion:::::' completer  _expand _complete _prefix _ignored _approximate # _expand expandiert dinge wie $FOO<Tab>, _complete ist
#das normale completion, _prefix ignoriert alles nach dem Cursor (für complete_in_word) _ignored ignoriered gewisse matches, ist mit
#_approximate wichtig, damit nicht falsche dinge completet werden, _approximate sucht nach ähnlichen Dingen
zstyle -e ':completion:*:approximate:*' max-errors 'reply=( $(( ($#PREFIX + $#SUFFIX) / 3 )) )' # maximal alle 3 zeichen ein fehler
zstyle ':completion:*:(^approximate):*' matcher-list 'm:{a-z}={A-Z}' # Kleinschreibung automatisch zu Großschreibung korrigieren.
zstyle ':completion:*:expand:*' keep-prefix yes #halt praefix behalten, HOME nicht zu cip/home blablabla expandierekn
zstyle ':completion:*' list-suffixes yes # completet a/b/c<tab> zu abc/bcd/coo
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS} # dircolors für completion
bindkey '^R' history-incremental-pattern-search-backward

#pipe
alias -g E='2>&1'
alias -g N='>/dev/null'
alias -g EN='2>/dev/null'
alias -g L='2>&1 | less'
alias -g G='| grep'
alias -g S='| sort'
alias -g ...='../..'
alias ..='cd ..'

#general shortcuts
alias psearch="apt-cache search"
alias i3lock="i3lock --image=/home/ik15ydit/.config/i3lock/bg.png"
#alias telegram='~/ciptmp/Zeug/Telegram/tg/bin/telegram-cli -k tg-server.pub'
alias x='startx'

#converting
alias -g jpg2png="echo 'use convert [file_in.jpg] [file_out.png]'" 

#cipstalk
alias w="ssh faui00n.cs.fau.de php /proj/ciptmp/av37umic/scripts/woist.php show" 
alias ww="ssh faui00n.cs.fau.de php /proj/ciptmp/av37umic/scripts/woist.php all" 
alias wa="ssh faui00n.cs.fau.de php /proj/ciptmp/av37umic/scripts/woist.php add" 
alias wd="ssh faui00n.cs.fau.de php /proj/ciptmp/av37umic/scripts/woist.php del" 
alias wl="ssh faui00n.cs.fau.de php /proj/ciptmp/av37umic/scripts/woist.php list"

#uni
alias irc="ssh ircbox.cs.fau.de -t 'command; tmux a'"
alias -g uni="faui06c.cs.fau.de"
alias cipkey="ssh-add ~/.ssh/ciplogin"

#direct to config
alias hlconf="vim ~/.config/herbstluftwm/autostart"
alias zshconf="vim ~/.zshrc"
alias vimconf="vim ~/.vimrc"

#ambigious aliases
alias dual="xrandr --output DVI-I-2 --right-of DVI-I-1"
alias shutown="/sbin/poweroff"
alias pcolor='for i in {0..255} ; do printf "\x1b[38;5;${i}mcolour${i} "; if [[ $(((($i+3)/6)*6)) -eq $(($i+3)) ]]; then echo; fi; done'

#aliases migrated from bashrc
alias spc='gcc -std=c99 -pedantic -Wall -Werror -D_XOPEN_SOURCE=700 -o'
alias woist='ssh ircbox nc localhost 1339 | grep -B1 " in .zshrci'
alias logins='nc localhost 1339 | grep -B1'
alias rudipub='cd /home/cip/2010/he29heri/pub/'
alias cltex="rm *.log *.aux *.fdb_latexmk *.fls"
alias wordcount="find . -type f -exec cat {} + | wc -w"

#ls and la
LS_COLORS=$LS_COLORS:'di=0;35:'; export LS_COLORS
alias la="ls -la --color=auto"
alias ll="ls -ll --color=auto"

#pipealiases
alias -g D='| dot -Tpng >'

gitssh=~/.ssh/gitrsa
function key(){
        eval `ssh-agent`
        ssh-add $gitssh
}
#export JAVA_HOME="/local/java-1.8"

#no write spam
mesg n
