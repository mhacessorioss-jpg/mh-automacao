"""Fotos de detalhe da peça (travertino + flores secas) para as colagens.

Uso: python -m mh.detalhes campanhas/black-friday [CODIGO ...]
Salva <campanha>/detalhes/<codigo>_1.png e _2.png
"""
import json, sys, time
from . import config, gemini
from .gerar_lote import produto

if __name__ == "__main__":
    pasta = config.RAIZ / sys.argv[1]
    so = set(sys.argv[2:])
    itens = json.loads((pasta / "itens.json").read_text(encoding="utf-8"))
    (pasta / "detalhes").mkdir(exist_ok=True)
    pr = config.PROMPTS["detalhe"]
    for it in itens:
        if so and it["codigo"] not in so:
            continue
        p = produto(it)
        ref = p.get("_ref") or (config.FOTOS / p["foto_peca"])
        base = pr["base"].format(nome=p["nome_vitrine"], cor=p["cor"], material=p["material"])
        for i, cena in enumerate(pr["cenas"], 1):
            saida = pasta / "detalhes" / f"{it['codigo']}_{i}.png"
            for t in range(2):
                try:
                    gemini.gerar_imagem(base + " " + cena, [ref], saida); print("ok", saida.name); break
                except Exception as e:
                    print("erro", saida.name, e); time.sleep(10)
