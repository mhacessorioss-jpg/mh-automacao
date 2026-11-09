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
    saida = config.RAIZ / "marca" / "modelo_oficial_sem_joias.png"
    gemini.gerar_imagem(PROMPT, [config.MODELO], saida)
    print("ok", saida)
