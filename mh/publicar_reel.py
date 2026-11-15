"""Publica um Reels. Uso: python -m mh.publicar_reel <video.mp4> <arquivo_legenda>"""
import sys
from . import config, instagram
if __name__ == "__main__":
    vid, leg = sys.argv[1], (config.RAIZ / sys.argv[2]).read_text(encoding="utf-8")
    print("Publicado:", instagram.publicar_reel(config.url_publica(vid), leg))
