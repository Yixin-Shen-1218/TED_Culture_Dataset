# ------------------------------------------------------------------------------
# Copyright (c) ETRI. All rights reserved.
# Licensed under the BSD 3-Clause License.
# This file is part of Youtube-Gesture-Dataset, a sub-project of AIR(AI for Robots) project.
# You can refer to details of AIR project at https://aiforrobots.github.io
# Written by Youngwoo Yoon (youngwoo@etri.re.kr)
# ------------------------------------------------------------------------------
import os

# class Config_Win:
#     # OPENPOSE_BASE_DIR = ".\mnt\eason\yixin\openpose\\"
#     # OPENPOSE_BIN_PATH = ".\mnt\eason\yixin\openpose\\bin\OpenPoseDemo.exe"
#     OPENPOSE_BASE_DIR = ".\mnt\eason\yixin\openpose\\"
#     OPENPOSE_BIN_PATH = "bin\OpenPoseDemo.exe"
#
#
# class TED_Culture_Config_Win(Config_Win):
#     # download raw video and subtitle data
#     language_list = ["Turkish", "French", "Italian", "Indonesian", "German", "Japanese"]
#
#     # language_codes = ["a.tr", "a.fr", "a.it", "a.id", "a.de", "a.ja"]
#     language_codes = ["tr", "fr", "it", "id", "de", "ja"]
#
#     playlist_urls = ["https://www.youtube.com/playlist?list=PLsRNoUx8w3rOWHcgwUTIio9PFxFEbIisd",
#                      "https://www.youtube.com/playlist?list=PLsRNoUx8w3rOzmp0qoc53u3vYrcFYsvKj",
#                      "https://www.youtube.com/playlist?list=PLsRNoUx8w3rMXlrHn6LWavbsKvnlgc1AN",
#                      "https://www.youtube.com/playlist?list=PLsRNoUx8w3rNkQEmDfmFlkLZQ0LLquMiq",
#                      "https://www.youtube.com/playlist?list=PLsRNoUx8w3rNZlOp1ceqLs76CSEWTSnFi",
#                      "https://www.youtube.com/playlist?list=PLsRNoUx8w3rOHjXIU5EE4KOiIagv9yQaG"]
#
#
#     # work path setting
#     WORK_PATH = '.\mnt\eason\yixin\TED_culture_Dataset'
#     # WORK_PATH = '..\TED_culture_Dataset'
#     CLIP_PATH = WORK_PATH + "\clip_ted"
#     VIDEO_PATH = WORK_PATH + "\\videos_ted"
#     METADATA_PATH = WORK_PATH + "\\video_csv"
#     METADATA_PATH_TXT = WORK_PATH + "\\video_ids"
#     SKELETON_PATH = WORK_PATH + "\skeleton_ted"
#     SUBTITLE_PATH = WORK_PATH + "\\video_subtitles"
#     OUTPUT_PATH = WORK_PATH + "\output"
#     SUBTITLE_TYPE = 'auto'
#     FILTER_OPTION = {"threshold": 100}

class Config_Linux:
    EXPOSE_BASE_DIR = "./mnt/eason/yixin/expose/"
    OPENPOSE_BASE_DIR = "./mnt/eason/yixin/openpose/"
    OPENPOSE_BIN_PATH = "build/examples/openpose/openpose.bin"


class TED_Culture_Config_Linux(Config_Linux):
    # download raw video and subtitle data
    language_list = ["Turkish", "French", "Italian", "Indonesian", "German", "Japanese"]

    # language_codes = ["a.tr", "a.fr", "a.it", "a.id", "a.de", "a.ja"]
    language_codes = ["tr", "fr", "it", "id", "de", "ja"]

    playlist_urls = ["https://www.youtube.com/playlist?list=PLsRNoUx8w3rOWHcgwUTIio9PFxFEbIisd",
                     "https://www.youtube.com/playlist?list=PLsRNoUx8w3rOzmp0qoc53u3vYrcFYsvKj",
                     "https://www.youtube.com/playlist?list=PLsRNoUx8w3rMXlrHn6LWavbsKvnlgc1AN",
                     "https://www.youtube.com/playlist?list=PLsRNoUx8w3rNkQEmDfmFlkLZQ0LLquMiq",
                     "https://www.youtube.com/playlist?list=PLsRNoUx8w3rNZlOp1ceqLs76CSEWTSnFi",
                     "https://www.youtube.com/playlist?list=PLsRNoUx8w3rOHjXIU5EE4KOiIagv9yQaG"]


    # work path setting
    WORK_PATH = './mnt/eason/yixin/TED_culture_Dataset'
    # WORK_PATH = '../TED_culture_Dataset'
    CLIP_PATH = WORK_PATH + "/clip_ted"
    VIDEO_PATH = WORK_PATH + "/videos_ted"
    METADATA_PATH = WORK_PATH + "/video_csv"
    METADATA_PATH_TXT = WORK_PATH + "/video_ids"
    SKELETON_PATH = WORK_PATH + "/skeleton_ted"
    SUBTITLE_PATH = WORK_PATH + "/video_subtitles"
    OUTPUT_PATH = WORK_PATH + "/output"
    MERGE_PATH = WORK_PATH + "/merge"
    AUDIO_PATH = WORK_PATH + '/audio_ted'
    EXPOSE_OUT_PATH = WORK_PATH + '/expose_ted'
    FILTER_PATH = WORK_PATH + '/filter_res'
    SUBTITLE_TYPE = 'auto'
    FILTER_OPTION = {"threshold": 100}


# SET THIS
my_config = TED_Culture_Config_Linux
