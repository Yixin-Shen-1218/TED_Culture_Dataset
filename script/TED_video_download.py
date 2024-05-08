import http.client
import os
import re
import socket
import time
import urllib

import pandas as pd
import shutup
import urllib3
import youtube_dl
from pytube import Playlist, YouTube
import csv

from pytube.exceptions import AgeRestrictedError

from config import my_config
import warnings


def subtitle_clean(subtitle_text, save_path):
    subtitle_text = subtitle_text.split('\n\n')
    sent_num = 1

    with open(save_path, 'w', encoding="utf-8") as f:
        for i in range((len(subtitle_text) - 1) // 2):
            _, temp_time, temp_text = subtitle_text[i * 2].split('\n')
            temp_start = temp_time.strip().split(' --> ')[0]
            _, next_time, _ = subtitle_text[(i + 1) * 2].split('\n')
            temp_end = next_time.strip().split(' --> ')[0]
            f.write(str(sent_num) + '\n')
            f.write(temp_start + ' --> ' + temp_end + '\n')
            f.write(temp_text.strip() + '\n')
            f.write('\n')
            sent_num += 1

        _, temp_time, temp_text = subtitle_text[-1].split('\n')
        f.write(str(sent_num) + '\n')
        f.write(temp_time + '\n')
        f.write(temp_text.strip() + '\n')


def video_filter(yt_info):
    passed = True

    exist_proper_format = False

    if yt_info.get("mime_type") == "video/mp4" and yt_info.get("res") == "720p" and yt_info.get(
            "vcodec") is not None and yt_info.get("acodec") is not None:
        exist_proper_format = True

    if not exist_proper_format:
        passed = False

    if passed:
        duration_minutes = float(yt_info.get("length")) / 60.0
        if duration_minutes < 5.0 or duration_minutes > 60.0:
            passed = False

    if passed:
        if yt_info.get("subtitle_content") is None:
            passed = False

    return passed


def subtitle_download(caption, vid, language, auto=True):
    if not auto:
        caption.download(title="{}-not_auto".format(vid), srt=True,
                         output_path=my_config.SUBTITLE_PATH + "/%s/" % language)
        # print(caption)
    else:
        caption.download(title="{}-auto".format(vid), srt=True,
                         output_path=my_config.SUBTITLE_PATH + "/%s/" % language)
        # print(caption)


def video_download():
    for language, language_code, playlist_url in zip(my_config.language_list, my_config.language_codes,
                                                     my_config.playlist_urls):
        download_count = 0
        skip_count = 0
        sub_count = 0
        auto_count = 0
        log = open("../log_dir/download_log_%s.txt" % language, 'w', encoding="utf-8")

        playlist = Playlist(playlist_url)

        print("The number of total videos in playlist:", len(playlist.video_urls))

        video_urls = playlist.video_urls

        # print("Total video_urls in playlist:", video_urls)

        title_list = []
        url_list = []
        vid_list = []

        number = 0

        for url in video_urls:
            yt = YouTube(url)
            title = yt.title
            vid = yt.video_id
            yt_info = {}
            number = number + 1
            print("this is the %d video" % number)

            # get the video length
            videoDetails = yt.vid_info.get("videoDetails")
            yt_info["length"] = videoDetails.get("lengthSeconds")

            try:
                highres_video = yt.streams.get_highest_resolution()
            except AgeRestrictedError:
                log.write("{}-{} - skipped\n".format(title, url))
                skip_count += 1
                print("This is the " + str(skip_count) + " skipped video")
                continue

            if highres_video is not None:
                # print(highres_video)
                # print(highres_video.resolution)
                # print(yt.captions.keys())
                # print(dict(yt.captions.keys()))
                # print(yt.captions.values())
                # print(len(yt.captions.keys()))

                # print(caption.xml_caption_to_srt(caption.generate_srt_captions()))
                # print(caption.xml_captions)
                # print(caption.generate_srt_captions())
                # print(caption)

                subtitle_content = yt.captions.get(language_code)

                yt_info["res"] = highres_video.resolution
                yt_info["vcodec"] = highres_video.video_codec
                yt_info["acodec"] = highres_video.audio_codec
                yt_info["mime_type"] = highres_video.mime_type
                yt_info["subtitle_content"] = subtitle_content

                # print("The false or ture value:", subtitle_content)
                # print(yt_info)

                if video_filter(yt_info):
                    try:
                        highres_video.download(output_path=my_config.VIDEO_PATH + "/%s" % language,
                                               filename=vid + '.mp4')
                    except http.client.IncompleteRead:
                        os.remove(my_config.VIDEO_PATH + "/%s" % language + "/" + vid + '.mp4')
                        print(
                            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!REMOVE THE FILE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" + vid + '.mp4')
                        log.write("{}-{} - skipped\n".format(title, url))
                        skip_count += 1
                        print("This is the " + str(skip_count) + " skipped video")
                        continue
                    download_count += 1

                    title_list.append(title)
                    url_list.append(url)
                    vid_list.append(vid)

                    caption = yt.captions.get_by_language_code(language_code)

                    # get caption and save it
                    # if the subtitle is provided
                    if "auto-generated" not in subtitle_content.name:
                        subtitle_download(caption, vid, language, auto=False)
                        sub_count += 1
                        print("This is the " + str(download_count) + " downloaded video" + ", and this is the " + str(
                            sub_count) + " not auto subtitle video")
                    else:
                        subtitle_download(caption, vid, language, auto=True)
                        auto_count += 1
                        print("This is the " + str(download_count) + " downloaded video" + ", and this is the " + str(
                            auto_count) + " auto subtitle video")

                    log.write("{}-{} - downloaded\n".format(title, url))
                else:
                    log.write("{}-{} - skipped\n".format(title, url))
                    skip_count += 1
                    print("This is the " + str(skip_count) + " skipped video")

            # # if the number of downloaded video is sufficient 200
            # if download_count == 200:
            #     break

            # if the number of downloaded video is sufficient 40
            if download_count == 40:
                break

        # print("Total video_titles after filter:", title_list)
        # print("Total number of videos after filter:", len(title_list))

        # write the downloaded video info into the csv file
        video_info_csv(title_list, url_list, vid_list, language)

        log.write("\nno of subtitles : {}\n".format(sub_count))
        log.write("\nno of auto-subtitles : {}\n".format(auto_count))
        log.write("\ndownloaded: {}, skipped : {}\n".format(download_count, skip_count))
        log.close()


def video_info_csv(title_list, url_list, vid_list, language):
    data_list = []
    for title, url, vid in zip(title_list, url_list, vid_list):
        x = {'title': title, 'video url': url, 'vid': vid}
        data_list.append(x)

    with open(my_config.METADATA_PATH + '/TED_%s_Video.csv' % language, 'w', newline='',
              encoding='UTF-8') as f_csv:
        writer = csv.writer(f_csv)
        writer.writerow(['title', 'video_url', 'vid'])
        for element in data_list:
            writer.writerow(element.values())


def make_dirs():
    if not os.path.exists(my_config.WORK_PATH):
        os.makedirs(my_config.WORK_PATH)

    for language in my_config.language_list:
        if not os.path.exists(my_config.WORK_PATH + "/videos_ted/" + language):
            os.makedirs(my_config.WORK_PATH + "/videos_ted/" + language)

        if not os.path.exists(my_config.WORK_PATH + "/video_subtitles/" + language):
            os.makedirs(my_config.WORK_PATH + "/video_subtitles/" + language)

        if not os.path.exists(my_config.WORK_PATH + "/video_csv"):
            os.makedirs(my_config.WORK_PATH + "/video_csv")

    if not os.path.exists("../log_dir"):
        os.makedirs("../log_dir")


def video_ids_txt_generate():
    if not os.path.exists(my_config.METADATA_PATH_TXT):
        os.makedirs(my_config.METADATA_PATH_TXT)

    for language in my_config.language_list:
        df = pd.read_csv(my_config.METADATA_PATH + '/TED_%s_Video.csv' % language)
        vid_list = list(df["vid"])

        wf = open(my_config.METADATA_PATH_TXT + "/video_%s_ids.txt" % language, "w")
        for j in vid_list:
            wf.write(str(j))
            wf.write('\n')
        wf.close()


def download_subtitle(url, filename, language, postfix):
    retry_delay = 2

    if not os.path.exists(my_config.SUBTITLE_PATH_vtt + "/" + language + "/" + '{}-{}.vtt'.format(filename, postfix)):
        # sleep the program to avoid HTTP Error 429
        time.sleep(30)
        urllib.request.urlretrieve(url, my_config.SUBTITLE_PATH_vtt + "/" + language + "/" + '{}-{}.vtt'.format(filename,
                                                                                                              postfix))


def subtitle_vtt_download():
    ydl_opts = {'format': 'best[height=720,ext=mp4]',
                'writesubtitles': True,
                'writeautomaticsub': True,
                'outtmpl': 'dummy.mp4'
                }  # download options

    video_ids_txt_generate()

    for language, language_code in zip(my_config.language_list, my_config.language_codes):
        print(language)
        if not os.path.exists(my_config.SUBTITLE_PATH_vtt + "/" + language):
            os.makedirs(my_config.SUBTITLE_PATH_vtt + "/" + language)

        vid_list = []
        with open(my_config.METADATA_PATH_TXT + "/video_%s_ids.txt" % language, "r") as f:
            for line in f.readlines():
                line = line.strip('\n')
                vid_list.append(line)

        vid_list = vid_list
        for i in range(len(vid_list)):
            ydl_opts['outtmpl'] = my_config.VIDEO_PATH + '/' + vid_list[i] + '.mp4'

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                vid = vid_list[i]
                url = "https://youtu.be/{}".format(vid)

                info = ydl.extract_info(url, download=False)

                # print(info)

                def get_subtitle_url(subtitles, language, ext):
                    subtitles = subtitles.get(language)
                    url = None
                    for sub in subtitles:
                        if sub.get('ext') == ext:
                            url = sub.get('url')
                            break
                    return url


                if info.get('subtitles') is not None and (info.get('subtitles')).get(language_code) is not None:
                    sub_url = get_subtitle_url(info.get('subtitles'), language_code, 'vtt')
                    # print(sub_url)
                    download_subtitle(sub_url, vid, language, language_code)
                    # print("!!!!!!!!!!!!!!!!!!!!!!!SUBCOUNT!!!!!!!!!!!!!!!!!!!!!!!")
                if info.get('automatic_captions') is not None:
                    auto_sub_url = get_subtitle_url(info.get('automatic_captions'), language_code, 'vtt')
                    download_subtitle(auto_sub_url, vid, language, language_code + '-auto')
                    # print("!!!!!!!!!!!!!!!!!!!!!!!AUTO!!!!!!!!!!!!!!!!!!!!!!!")


if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    shutup.please()
    # make_dirs()
    # video_download()
    # subtitle_vtt_download()
