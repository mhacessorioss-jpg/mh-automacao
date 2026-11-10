"""Edita uma imagem com o Gemini. Uso: python -m mh.editar <entrada> <saida> <arquivo_com_instrucao>"""
import sys
from . import config, gemini
if __name__ == "__main__":
    e, s, p = (config.RAIZ / a for a in sys.argv[1:4])
    gemini.gerar_imagem(p.read_text(encoding="utf-8"), [e], s); print("ok", s)
