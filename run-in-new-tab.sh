#! /bin/sh

window="$(xdotool search --class gnome-terminal | head -1)"
xdotool windowfocus $window
xdotool key ctrl+shift+t
xdotool type "$*"
xdotool key Return