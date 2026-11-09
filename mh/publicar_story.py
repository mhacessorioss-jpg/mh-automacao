"""Publica um Story no Instagram a partir de uma imagem do repositório.

Uso: python -m mh.publicar_story fila/AN3267-1/story.jpg
"""
import sys, time
from . import config, instagram

if __name__ == "__main__":
    caminho = sys.argv[1]
    url = config.url_publica(caminho) + f"?v={int(time.time())}"
    print("Story publicado:", instagram.publicar_foto(url, story=True))
