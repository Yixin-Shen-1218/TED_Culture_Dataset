# ------------------------------------------------------------------------------
# Copyright (c) ETRI. All rights reserved.
# Licensed under the BSD 3-Clause License.
# This file is part of Youtube-Gesture-Dataset, a sub-project of AIR(AI for Robots) project.
# You can refer to details of AIR project at https://aiforrobots.github.io
# Written by Youngwoo Yoon (youngwoo@etri.re.kr)
# ------------------------------------------------------------------------------
from datetime import datetime


class Config:
    DEVELOPER_KEY = "AIzaSyCitmDSHacAy1Pc1Z1qKAPegEgVuRw-qXc"  # your youtube developer id
    OPENPOSE_BASE_DIR = "./mnt/eason/yixin/openpose/"
    OPENPOSE_BIN_PATH = "./mnt/eason/yixin/openpose/bin/OpenPoseDemo.exe"


class TED_Culture_Config(Config):
    YOUTUBE_CHANNEL_ID = "UCAuUUnT6oDeKwE6v1NGQxug"

    # Final Language List, download raw video and subtitle data
    language_list = ["Turkish", "French", "Italian", "Indonesian", "German", "Japanese"]

    language_codes = ["tr", "fr", "it", "id", "de", "ja"]

    playlist_urls = ["https://www.youtube.com/playlist?list=PLsRNoUx8w3rOWHcgwUTIio9PFxFEbIisd",
                     "https://www.youtube.com/playlist?list=PLsRNoUx8w3rOzmp0qoc53u3vYrcFYsvKj",
                     "https://www.youtube.com/playlist?list=PLsRNoUx8w3rMXlrHn6LWavbsKvnlgc1AN",
                     "https://www.youtube.com/playlist?list=PLsRNoUx8w3rNkQEmDfmFlkLZQ0LLquMiq",
                     "https://www.youtube.com/playlist?list=PLsRNoUx8w3rNZlOp1ceqLs76CSEWTSnFi",
                     "https://www.youtube.com/playlist?list=PLsRNoUx8w3rOHjXIU5EE4KOiIagv9yQaG"]

    # work path setting
    WORK_PATH = './mnt/eason/yixin/TED_culture_Dataset'
    CLIP_PATH = WORK_PATH + "/clip_ted"
    VIDEO_PATH = WORK_PATH + "/videos_ted"
    METADATA_PATH = WORK_PATH + "/video_csv"
    SKELETON_PATH = WORK_PATH + "/skeleton_ted"
    SUBTITLE_PATH = WORK_PATH + "/video_subtitles"
    OUTPUT_PATH = WORK_PATH + "/output"
    VIDEO_SEARCH_START_DATE = datetime(2011, 3, 1, 0, 0, 0)

    # language_list = ["Japanese"]
    #
    # language_codes = ["a.ja"]
    #
    # playlist_urls = ["https://www.youtube.com/playlist?list=PLsRNoUx8w3rOHjXIU5EE4KOiIagv9yQaG"]


# SET THIS
my_config = TED_Culture_Config
