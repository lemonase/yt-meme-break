#!/usr/bin/env python
from datetime import datetime, timedelta
import logging
import os
import random
import subprocess
import sys
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerNotRunningError
import pystray
from PIL import Image, ImageDraw, ImageColor

from playlists import MEME_PLAYLISTS
from youtube_dl import YoutubeDL

BREAK_INTERVAL_MIN = 30
TICK_INTERVAL_SEC = 5
seconds_passed = 0

start_datetime = datetime.now()
stop_datetime = timedelta(minutes=BREAK_INTERVAL_MIN)
stop_seconds = timedelta.total_seconds(stop_datetime)

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
    try:
        info = ydl.extract_info(playlist_url, download=False)
    except:
        logging.error("Erorr getting playlist info")

    return info


def get_yt_meme_url():
    """ Picks a random video from a choice of meme_playlists """

    # get the randy playlist
    yt_watch_prefix = "https://www.youtube.com/watch?v="
    random_pl = random.choice(MEME_PLAYLISTS)

    # get playlist info for a random playlist
    pl_info = get_playlist_info(random_pl)

    # get random url from entries in the playlist
    random_video_url = yt_watch_prefix + str(
        random.choice(pl_info["entries"])["url"])

    return str(random_video_url)


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
    try:
        scheduler.shutdown(wait=False)
    except SchedulerNotRunningError as E:
        print("Scheduler Erorr:", E)

    os._exit(1)


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


def open_video():
    yt_vid = get_yt_meme_url()

    try:
        if sys.platform.startswith("darwin"):
            subprocess.run(["open", yt_vid], check=False)
        elif sys.platform.startswith("win32"):
            os.startfile(yt_vid)
        elif sys.platform.startswith("linux"):
            subprocess.run(["xdg-open", yt_vid], check=False)
        else:
            sys.exit("Unknown platform")
    except:
        print("Error Opening Video")


def update_menus(icon):
    # menu must be converted to a list to be mutable
    menu_list = list(icon.menu)
    menu_list[3] = pystray.MenuItem(
        'Time Passed: {}min {}sec'.format(get_min_passed(), get_sec_passed()),
        get_sec_passed)
    icon.menu = tuple(menu_list)


def tick(interval, icon):
    global seconds_passed
    seconds_passed = seconds_passed + interval

    update_menus(icon)

    if seconds_passed >= stop_seconds:
        open_video()
        icon.notify("Get up and stretch!")
        reset_timer()


def init_schedulers(picon):
    scheduler.start()

    scheduler.add_job(tick,
                      'interval', (TICK_INTERVAL_SEC, picon),
                      seconds=TICK_INTERVAL_SEC, id="TICK")

    picon.run()


def main():
    picon = create_icon()
    init_schedulers(picon)


if __name__ == '__main__':
    main()
