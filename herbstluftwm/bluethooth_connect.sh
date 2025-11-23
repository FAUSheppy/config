#!/usr/bin/env bash

SESSION="btconnect"
MAC="E8:9E:13:04:0A:77"

if [[ "$1" == "d" ]]; then
    CMD="disconnect $MAC"
else
    CMD="connect $MAC"
fi

tmux new-session -d -s "$SESSION" "bluetoothctl"

sleep 0.3

tmux send-keys -t "$SESSION" "$CMD" C-m
tmux send-keys -t "$SESSION" C-d
