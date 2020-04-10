# yt-meme-break.py

A fun reminder to take a break from sitting and staring at a monitor.

## This script depends on [youtube-dl](https://github.com/ytdl-org/youtube-dl/).

### Installing youtube-dl

If you have pip or homebrew, you can:
`pip install youtube_dl` or `brew install youtube-dl`

*NOTE:* youtube-dl is used only to get playlist information, and does not actually download any videos

## Usage

```
usage: yt-meme-break.py [-h] [-t TIME] [-p PLAYER] [-d DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  -t TIME, --time TIME  The time to wait in minutes (default is 30)
  -p PLAYER, --player PLAYER
                        The video player COMMAND you wish to use to play the youtube video
  -d DIRECTORY, --directory DIRECTORY
                        Play a video from a directory instead of youtube
```

## Running in the background

### Linux and MacOS

On Linux or macOS, you can simply run:

```sh
python yt-meme-break.py &
```

To kill the process, you can run

```sh
pkill -f yt-meme-break.py
```

### Windows

On Windows, you can use the `pythonw.exe` interperter

```cmd
pythonw yt-meme-break.py
```

To kill the process, you can use Task Manager.

## Videos

These are the playlists in playlists.py

If you have a suggestion, please send a PR.

### Youtube Playlists

- ["Memes / Sound Bites"](https://www.youtube.com/watch?v=umDr0mPuyQc&list=PLQ0Mnj2iCeGxNTaAtuoppV7YAKM_qFb5a&index=1) by Brett Thornburg (1 / 82 )
- ["Memes and soundbites"](https://www.youtube.com/watch?v=_RpgbZcHk_A&list=PLljLVBd4na8x68p6jfAJV7HXJpcXOiLWC&index=1) by R. M. Fox (1 / 22)
- ["Meme Sounds"](https://www.youtube.com/watch?v=xjPXvy4WKHA&list=PLPbYmF3GfbKhKZKdu551Lq776n9-Qsnlc&index=1) by Zackden Lau (1 / 74)
- ["Memes worth using in videos"](https://www.youtube.com/watch?v=djV11Xbc914&list=PLm5ic07toZes0gvNYcwRAysK_G2AFlvdf&index=1) by Atrm1353 (1 / 199)
- ["Memes/Sound Bites"](https://www.youtube.com/watch?v=0nrdZsm__XY&list=PLaKMdWQ0aU2g2oG4-mol2RYdebexfIw6c&index=2) by Azron945 (2 / 210)
- ["meme sounds"](https://www.youtube.com/watch?v=kk0feCp_MZ4&list=PLsjLCKJRALYVEm-kLRdVwNY7eLm6VNCCK&index=1) by shokk (1 / 126)

### Youtube Mixes

#### YTP

- ["PragerU YTP"](https://www.youtube.com/watch?v=rG_Ue3t17l0&list=RDrG_Ue3t17l0&index=1)

#### Content Aware Scale

- [MrMrMANGOHEAD](https://www.youtube.com/watch?v=nX7ObbHCd7M&list=RDCMUCKNNYHhX5md5nMN3do15Yiw&index=1)
- [Husband Calling Contest](https://www.youtube.com/watch?v=7UTgzCb6JPg&list=RD7UTgzCb6JPg&index=1)

#### Horrible Reneditions Of Songs

- [Magik Mike](https://www.youtube.com/watch?v=HwoJheyM1Zs&list=RDHwoJheyM1Zs&index=1)

#### Parody Songs

- [Trevor Moore - Mouthwash](https://www.youtube.com/watch?v=_YNgRRyRxK0&list=RD_YNgRRyRxK0&index=1)

### Note about youtube-dl and mixes

I have not looked too much into it, but there seems to be some limitations with either
`youtube-dl` or the YouTube API, but for some reason, mixes take much longer to query
than regular playlists.
