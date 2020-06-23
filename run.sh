#!/bin/bash

if [ "$1" == "tray" ]; then
  nohup python yt-meme-break-systray.py > /tmp/yt-meme.log &
else
  nohup python yt-meme-break.py &> /tmp/yt-meme.log &
fi

