# yt-meme-break

Periodically play a random youtube meme as a reminder to take a break from sitting at the dang computer.

## Requirements

```sh
pip install -r requirements.txt
```

## yt-meme-break-systray.py

Creates a system tray icon and starts a timer that will notify and open a video
from a random youtube meme playlist after a specified interval.

### Usage

On Linux

```sh
$ nohup python yt-meme-break-systray.py > /tmp/yt-meme.log &
```

On Windows

```cmd
C:\> pythonw yt-meme-break-systray.py
```
