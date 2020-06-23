#!/usr/bin/env python
from datetime import datetime, timedelta
import random
import subprocess
import sys
import time

from apscheduler.schedulers.background import BackgroundScheduler
import pystray
from PIL import Image, ImageDraw, ImageColor

from playlists import MEME_PLAYLISTS
from youtube_dl import YoutubeDL

# times
seconds_passed = 0
break_interval = 30
tick_interval = 1

# datetimes
start_datetime = datetime.now()
stop_datetime = timedelta(minutes=break_interval)
stop_seconds = timedelta.total_seconds(stop_datetime)

# scheduler
scheduler = BackgroundScheduler()


def get_playlist_info(playlist_url):
    """ Takes a url for a playlist and returns info about it """
    # setup ydl options
    ydl_opts = {
        "simulate": True,
        "ignore_errors": True,
        "extract_flat": True,
        "quiet": True,
    }

    # init YoutubeDL object
    ydl = YoutubeDL(ydl_opts)
    ydl.add_default_info_extractors()

    # get video info
    info = ydl.extract_info(playlist_url, download=False)

    return info


def get_random_yt_video():
    """ Picks a random video from a choice of meme_playlists """

    yt_watch_prefix = "https://www.youtube.com/watch?v="
    random_pl = random.choice(MEME_PLAYLISTS)

    # get playlist info for a random playlist
    pl_info = get_playlist_info(random_pl)

    # get random url from entries in the playlist
    random_video_url = yt_watch_prefix + str(
        random.choice(pl_info["entries"])["url"])

    return random_video_url


def pause_timer():
    scheduler.pause()


def resume_timer():
    scheduler.resume()


def reset_timer():
    global seconds_passed
    seconds_passed = 0


def get_sec_passed():
    return int(seconds_passed % 60)


def get_min_passed():
    return int(seconds_passed // 60)


def get_interval():
    return int(stop_seconds)


def set_interval(minutes):
    pass


def exit_app():
    scheduler.shutdown()
    sys.exit()


def create_icon():
    # create images
    pyimg = Image.open('images/py.png')
    pyimg.thumbnail((128, 128))

    # create menus
    menu = (pystray.MenuItem('Pause Timer', pause_timer),
            pystray.MenuItem('Resume Timer', resume_timer),
            pystray.MenuItem('Reset Timer', reset_timer),
            pystray.MenuItem(
                'Time Passed: {}min {}sec'.format(get_min_passed(),
                                                  get_sec_passed()),
                get_sec_passed),
            pystray.MenuItem(
                'Break Interval {}min {}sec'.format(get_interval() // 60,
                                                    get_interval() % 60),
                set_interval),
            pystray.MenuItem('Quit', exit_app))

    # create icon
    icon = pystray.Icon('YT Timer', pyimg, 'YT Timer', menu)
    icon.visible = True

    return icon


def update_menus(icon):
    # print('Time Passed: {}:{}'.format(get_min_passed(), get_sec_passed()))

    # menu must be converted to a list to be mutable
    menu_list = list(icon.menu)
    menu_list[3] = pystray.MenuItem(
        'Time Passed: {}min {}sec'.format(get_min_passed(), get_sec_passed()),
        get_sec_passed)
    icon.menu = tuple(menu_list)


def open_video():
    yt_vid = get_random_yt_video()
    cmd = ["chromium", str(yt_vid)]
    print("Opening youtube video: ", yt_vid)
    subprocess.run(cmd, check=False)


def tick(interval):
    global seconds_passed
    seconds_passed = seconds_passed + interval

    if seconds_passed >= stop_seconds:
        open_video()
        reset_timer()


def init_schedulers(picon):
    global scheduler, tick_interval
    scheduler.add_job(tick,
                      'interval', (tick_interval, ),
                      seconds=tick_interval)
    scheduler.add_job(update_menus,
                      'interval', (picon, ),
                      seconds=tick_interval)

    # start tick timer and run pystray
    scheduler.start()
    picon.run()


def main():
    picon = create_icon()
    init_schedulers(picon)


if __name__ == '__main__':
    main()
