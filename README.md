# yt-meme-break

Periodically play a random youtube meme as a reminder to take a break from sitting at the dang computer.

## Requirements

```sh
pip install -r requirements.txt
```

## yt-meme-break-systray.py

Creates a icon in the system tray that can be used to control the timer.

### Usage

```sh
nohup python yt-meme-break-systray.py > /tmp/yt-meme.log &
```

## yt-meme-break.py

A basic script version

**NOTE:**[youtube-dl](https://github.com/ytdl-org/youtube-dl/) is used only to get playlist information, and does not actually download any videos

### Usage

```txt
usage: yt-meme-break.py [-h] [-t TIME] [-p PLAYER] [-d DIRECTORY] [-o] [-k]

optional arguments:
  -h, --help            show this help message and exit
  -t TIME, --time TIME  The time to wait in minutes (default is 30)
  -p PLAYER, --player PLAYER
                        The video player COMMAND you wish to use to play the youtube video
  -d DIRECTORY, --directory DIRECTORY
                        Play a video from a directory instead of youtube
  -o, --once            Play a single video and quit
  -k, --kill            Kill yt-meme-break process if it is running in the background
```

### Running in the background

### Linux and MacOS

On Linux or macOS, you can simply run:

```sh
nohup python yt-meme-break.py &> /tmp/yt-meme.log &
```

To kill the process, you can run either:

```sh
python yt-meme-break.py -k
```

or

```sh
pkill -f yt-meme-break.py
```

### Windows

On Windows, you can use the `pythonw.exe` interpreter to run in the background

```sh
pythonw.exe yt-meme-break.py
```

To kill the process, you can use Task Manager or run `yt-meme-break.py -k`

### Note about youtube-dl and mixes

I have not looked too much into it, but there seems to be some limitations with either
`youtube-dl` or the YouTube API, but for some reason, mixes take much longer to query
than regular playlists.
