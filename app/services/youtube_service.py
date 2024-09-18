from googleapiclient.discovery import build
import yt_dlp
import logging
from app.core.config import settings

API_KEY = settings.API_KEY
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def download_audio(video_url: str, output_path: str):
    logger.info(f"Downloading audio from URL: {video_url}")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}.%(ext)s',  
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def search_youtube(song_name: str):
    logger.info(f"Searching YouTube for song: {song_name}")
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.search().list(
        q=song_name,
        part='snippet',
        maxResults=1,
        type='video'
    )
    response = request.execute()
    if not response['items']:
        logger.warning("No results found on YouTube.")
        return None
    video_id = response['items'][0]['id']['videoId']
    return f'https://www.youtube.com/watch?v={video_id}'