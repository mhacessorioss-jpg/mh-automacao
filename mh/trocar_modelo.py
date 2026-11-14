"""Troca a modelo das fotos reais do fornecedor pela modelo da marca, mantendo os brincos.
Uso: python -m mh.trocar_modelo campanhas/trios-real/lista.json"""
import json, sys, time
from . import config, gemini
if __name__ == "__main__":
    lista = json.loads((config.RAIZ / sys.argv[1]).read_text(encoding="utf-8"))
    prompt = (config.RAIZ / "campanhas/trios-real/prompt_troca.txt").read_text(encoding="utf-8")
    for it in lista:
        s = config.RAIZ / it["saida"]
        if s.exists(): continue
        for t in range(2):
            try:
                gemini.gerar_imagem(prompt, [config.RAIZ / it["entrada"], config.RAIZ / it["ref"]], s); print("ok", s.name); break
            except Exception as e:
                print("erro", it["codigo"], e); time.sleep(10)
