"""Publica um vídeo como Story. Uso: python -m mh.publicar_story_video <video.mp4>"""
import sys, time
from . import config, instagram
if __name__ == "__main__":
    url = config.url_publica(sys.argv[1]) + f"?v={int(time.time())}"
    print("Story (vídeo) publicado:", instagram.publicar_reel(url, story=True))
