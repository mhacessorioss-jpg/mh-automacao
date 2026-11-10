"""Gera, uma única vez, a foto de referência da modelo oficial SEM nenhuma joia.

Uso: python -m mh.limpar_modelo
Salva em marca/modelo_oficial_sem_joias.png (depois de conferida, vira a referência).
"""
from . import config, gemini

PROMPT = (
    "Recrie esta MESMA foto, da MESMA mulher, mantendo exatamente o rosto, os traços, o tom de pele, "
    "o cabelo, a maquiagem, a roupa, a pose, o fundo e a luz. A ÚNICA mudança: remova TODAS as joias e "
    "acessórios (colares, brincos, ear cuffs, piercings, anéis, pulseiras). Orelhas, pescoço e mãos "
    "devem ficar completamente sem joias. Foto fotorrealista, formato vertical."
)

if __name__ == "__main__":
    import sys
    from pathlib import Path
    # Uso opcional: python -m mh.limpar_modelo <entrada> <saida>
    entrada = config.RAIZ / sys.argv[1] if len(sys.argv) > 1 else config.MODELO
    saida = config.RAIZ / sys.argv[2] if len(sys.argv) > 2 else config.RAIZ / "marca" / "modelo_oficial_sem_joias.png"
    gemini.gerar_imagem(PROMPT, [entrada], saida)
    print("ok", saida)
