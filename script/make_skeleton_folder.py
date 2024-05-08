import glob
import json
import os
import pickle
import subprocess

import shutil

from config import my_config

OUTPUT_SKELETON_PATH = my_config.WORK_PATH + "/temp_skeleton_raw"

def get_vid_from_filename(filename):
    return filename[-15:-4]


if __name__ == '__main__':

    if not os.path.exists(OUTPUT_SKELETON_PATH):
        os.makedirs(OUTPUT_SKELETON_PATH)

    video_files = glob.glob(my_config.VIDEO_PATH + "/*.mp4")

    for file in sorted(video_files, key=os.path.getmtime):
        print(file)
        vid = get_vid_from_filename(file)
        print(vid)

        # create out dir
        skeleton_dir = OUTPUT_SKELETON_PATH + "/" + vid + "/"
        if not os.path.exists(skeleton_dir):
            os.makedirs(skeleton_dir)

        if os.path.exists(skeleton_dir + "keypoints/"):
            shutil.rmtree(skeleton_dir + "keypoints/")

        os.makedirs(skeleton_dir + "keypoints/")

        skeleton_files = glob.glob(skeleton_dir + "/*.json")
        # print(skeleton_files)

        for skeleton_file in sorted(skeleton_files, key=os.path.getmtime):
            print(skeleton_file)
            move_command = "mv" + " " + skeleton_file + " " + skeleton_dir + "keypoints/"
            subprocess.call(move_command, shell=True)

