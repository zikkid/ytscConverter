import os
from pytube import YouTube
from pytube.exceptions import RegexMatchError
from sclib import SoundcloudAPI
import requests
import re

def convert_to_mp3(url, output_dir=None):
    try:
        if "youtube.com" in url:
            youtube = YouTube(url)
            video = youtube.streams.filter(only_audio=True).first()

            if output_dir:
                mp3_file = os.path.join(output_dir, f"{youtube.title}.mp3")
            else:
                mp3_file = os.path.join(os.path.expanduser('~'), 'Downloads', f"{youtube.title}.mp3")

            video.download(output_path=output_dir)
            os.replace(video.default_filename, mp3_file)

            print(f"conversion complete: {mp3_file}")
        elif "soundcloud.com" in url:
            api = SoundcloudAPI()

            track = api.resolve(url)
            stream_url = track.STREAM_URL

            if output_dir:
                mp3_file = os.path.join(output_dir, f"{track.artist} - {track.title}.mp3")
            else:
                mp3_file = os.path.join(os.path.expanduser('~'), 'Downloads', f"{track.artist} - {track.title}.mp3")

            response = requests.get(stream_url)
            with open(mp3_file, 'wb') as file:
                file.write(response.content)

            print(f"conversion complete: {mp3_file}")
        else:
            print("invalid link: unsupported platform")
    except RegexMatchError:
        print("invalid youtube URL")
    except Exception as e:
        print(f"an error occured: {e}")

def process_file(file_path):
    youtube_regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.?be)\/(?:watch\?v=)?([a-zA-Z0-9_-]{11})'
    soundcloud_regex = r'(?:https?:\/\/)?(?:www\.)?(?:soundcloud\.com)\/([a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+)'


    with open(file_path, 'r') as file:
        for line in file:
            link = line.strip()

            if line.startswith("#"):
                continue

            if re.match(youtube_regex, link) or re.match(soundcloud_regex, link):
                convert_to_mp3(link)
            else:
                print(f"ignoring unsupported url: {link}")

file_path = './links.txt'
process_file(file_path)
