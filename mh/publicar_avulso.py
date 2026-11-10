"""Publica um post avulso no feed. Uso: python -m mh.publicar_avulso <imagem> <arquivo_legenda> [colaborador ...]"""
import sys
from . import config, instagram
if __name__ == "__main__":
    img, leg = sys.argv[1], (config.RAIZ / sys.argv[2]).read_text(encoding="utf-8")
    print("Publicado:", instagram.publicar_foto(config.url_publica(img), leg, colaboradores=sys.argv[3:] or None))
