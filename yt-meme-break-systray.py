#!/usr/bin/env python
import logging
import os
import random
import subprocess
import sys
import time
from datetime import datetime, timedelta

import pystray
import requests
from apscheduler.schedulers import SchedulerNotRunningError
from apscheduler.schedulers.background import BackgroundScheduler
from PIL import Image, ImageColor, ImageDraw

BREAK_INTERVAL_MIN = 30
TICK_INTERVAL_SEC = 5
seconds_passed = 0

start_datetime = datetime.now()
stop_datetime = timedelta(minutes=BREAK_INTERVAL_MIN)
stop_seconds = timedelta.total_seconds(stop_datetime)

scheduler = BackgroundScheduler()

api_url = "https://youtube-meme-api.herokuapp.com"
video_url_prefix = "https://www.youtube.com/watch?v="

endpoints = {
    "video": "/api/v1/random/video",
    "playlist": "/api/v1/random/playlist",
    "playlist_item": "/api/v1/random/playlist/item",
    "channel": "/api/v1/random/channel",
}

aggregate_endpoints = {
    "video": "/api/v1/all/video",
    "playlist": "/api/v1/all/playlist",
    "playlist_item": "/api/v1/all/playlist/item",
    "channel": "/api/v1/all/channel",
}


def get_random_yt_video():
    """ Picks a random video from api """
    r = requests.get(api_url + endpoints["playlist_item"])
    r.raise_for_status()
    vid_id = r.json()["contentDetails"]["videoId"]

    return video_url_prefix + vid_id


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
    pyimg = Image.open("images/py.png")
    pyimg.thumbnail((128, 128))

    # create menus
    menu = (
        pystray.MenuItem("Pause Timer", pause_timer),
        pystray.MenuItem("Resume Timer", resume_timer),
        pystray.MenuItem("Reset Timer", reset_timer),
        pystray.MenuItem(
            "Time Passed: {}min {}sec".format(get_min_passed(), get_sec_passed()),
            get_sec_passed,
        ),
        pystray.MenuItem(
            "Break Interval {}min {}sec".format(
                get_interval() // 60, get_interval() % 60
            ),
            set_interval,
        ),
        pystray.MenuItem("Quit", exit_app),
    )

    # create icon
    icon = pystray.Icon("YT Timer", pyimg, "YT Timer", menu)
    icon.visible = True

    return icon


def open_video():
    yt_vid = get_random_yt_video()

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
        "Time Passed: {}min {}sec".format(get_min_passed(), get_sec_passed()),
        get_sec_passed,
    )
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

    scheduler.add_job(
        tick,
        "interval",
        (TICK_INTERVAL_SEC, picon),
        seconds=TICK_INTERVAL_SEC,
        id="TICK",
    )

    picon.run()


def main():
    picon = create_icon()
    init_schedulers(picon)


if __name__ == "__main__":
    main()
