#
# ~/.bash_profile
#
xrandr --output HDMI-A-0 --auto --left-of DisplayPort-0 &
xbindkeys &
setxkbmap -option caps:escape
[[ -f ~/.bashrc ]] && . ~/.bashrc
