#!/usr/bin/env python3
"""
A script to play a random youtube video from a random playlist periodically
"""

import argparse
import os
import random
import subprocess
import sys
import time

import psutil
import requests

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
    """ Picks a random youtube video from api """
    r = requests.get(api_url + endpoints["playlist_item"])
    r.raise_for_status()
    vid_id = r.json()["contentDetails"]["videoId"]

    return video_url_prefix + vid_id


def get_random_local_video(meme_dir):
    """ Plays local videos """
    return os.path.join(meme_dir, random.choice(os.listdir(meme_dir)))


def get_default_player():
    """ Returns the default 'file opener' for each platform """
    file_opener = ""
    if sys.platform.startswith("darwin"):
        file_opener = "open"
    elif sys.platform.startswith("win32"):
        file_opener = "rundll32 url.dll,FileProtocolHandler"
    elif sys.platform.startswith("linux"):
        file_opener = "xdg-open"
    else:
        sys.exit("Unknown platform")
    return file_opener


def kill_bg_processes():
    """ Kills all python processes with 'yt-meme-break' in their argument list """
    for proc in psutil.process_iter():
        if proc.name().startswith("py"):
            if proc.pid == os.getpid() or proc.pid == os.getppid():
                continue
            for arg in proc.cmdline():
                if "yt-meme-break" in arg:
                    print(f"Killing PID: {proc.pid}")
                    try:
                        proc.kill()
                    except:
                        print(f"Could not kill {proc.pid}")


def main():
    """ Main func """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t", "--time", help="The time to wait in minutes (default is 30)", type=int,
    )
    parser.add_argument(
        "-p",
        "--player",
        help="The video player COMMAND you wish to use to play the youtube video",
        type=str,
    )
    parser.add_argument(
        "-d", "--directory", help="Play a video from a directory instead of youtube"
    )
    parser.add_argument(
        "-o",
        "--once",
        default=False,
        action="store_true",
        help="Play a single video and quit",
    )
    parser.add_argument(
        "-k",
        "--kill",
        action="store_true",
        help="Kill yt-meme-break process if it is running in the background",
    )

    args = parser.parse_args()

    # set arg defaults
    sleep_minutes = 30
    video_player_cmd = list(get_default_player().split())
    user_directory = ""

    # gather args
    if args.time:
        sleep_minutes = args.time

    if args.player:
        video_player_cmd = args.player.split()

    if args.directory:
        user_directory = args.directory

    if args.kill:
        kill_bg_processes()
        sys.exit(0)

    # run once
    if args.once:
        if user_directory:
            url = get_random_local_video(user_directory)
        else:
            url = get_random_yt_video()

        url = [url]

        subprocess.run(video_player_cmd + url, check=False)
    else:
        # main loop
        print(f"Starting with PID [{os.getpid()}]")
        while True:
            time.sleep(sleep_minutes * 60)

            if user_directory:
                url = get_random_local_video(user_directory)
            else:
                url = get_random_yt_video()

            url = [url]

            subprocess.run(video_player_cmd + url, check=False)


if __name__ == "__main__":
    main()
