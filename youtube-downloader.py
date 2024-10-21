#!/opt/miniconda3/bin/python

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title YouTube Downloader
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 🤖
# @raycast.argument1 { "type": "text", "placeholder": "URL", "optional": false }
# @raycast.argument2 { "type": "dropdown", "placeholder": "action", "data": [{"title": "pobierz film", "value": "1"}, {"title": "pobierz mp3", "value": "2"}, {"title": "skopiuj napisy", "value": "3"}]}

# Documentation:
# @raycast.author minis
# @raycast.authorURL https://raycast.com/minis

import sys
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import pyperclip

# Konfiguracja opcji pobierania wideo
yt_dlp_opts_video = {
    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
    "outtmpl": "~/Desktop/%(title)s.%(ext)s",
    "postprocessors": [
        {
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4",  # Wymuszenie na mp4, jeśli konwersja jest konieczna
        }
    ],
}

# Konfiguracja opcji pobierania audio
yt_dlp_opts_audio = {
    "format": "bestaudio/best",
    "outtmpl": "~/Desktop/%(title)s.%(ext)s",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}


def get_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed_url.query)["v", None][0]
    elif parsed_url.hostname in ["youtu.be"]:
        return parsed_url.path[1:]
    return None


def download_video(url):
    """Pobiera wideo z YouTube"""
    with yt_dlp.YoutubeDL(yt_dlp_opts_video) as ydl:
        ydl.download([url])
    print("Video downloaded successfully!")


def download_audio(url):
    """Pobiera audio z YouTube"""
    with yt_dlp.YoutubeDL(yt_dlp_opts_audio) as ydl:
        ydl.download([url])
    print("Audio downloaded successfully!")


def copy_transcript(video_id):
    """Kopiuje napisy z YouTube"""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=["pl", "en"]
        )
        text = " ".join(item["text"].replace("\n", "") for item in transcript)
        pyperclip.copy(text)
        print("Skopiowano do schowka...")
    except Exception as e:
        print(f"Błąd przy pobieraniu napisów: {str(e)}")


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else None
    user_input = sys.argv[2] if len(sys.argv) > 2 else None

    if not url:
        print("Podany URL jest niepoprawny. Spróbuj ponownie.")
        return

    video_id = get_video_id(url)
    if not video_id:
        print("Podany URL jest niepoprawny. Spróbuj ponownie.")
        return

    if user_input == "1":
        download_video(url)
    elif user_input == "2":
        download_audio(url)
    elif user_input == "3":
        copy_transcript(video_id)
    else:
        print("Nieznana opcja, spróbuj ponownie...")


if __name__ == "__main__":
    main()
