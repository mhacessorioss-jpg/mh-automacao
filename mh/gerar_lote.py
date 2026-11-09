"""Gera fotos na modelo oficial para uma campanha (sem abrir pedidos de aprovação).

Uso: python -m mh.gerar_lote campanhas/black-friday [CODIGO ...]
Lê <campanha>/itens.json e salva <campanha>/fotos/<codigo>.png
"""
import json, sys, time
from pathlib import Path
from . import config, estado, gemini, gerar


def produto(item):
    if item["codigo"] == "RELOGIO" or item.get("ref"):
        return {"codigo": item["codigo"], "nome_vitrine": item["nome"], "categoria": item["categoria"],
                "cor": item.get("cor", "dourado"), "material": item.get("material", ""),
                "foto_peca": None, "foto_em_uso": "", "_ref": config.RAIZ / item["ref"]}
    return estado.proximo_produto(item["codigo"])


if __name__ == "__main__":
    pasta = config.RAIZ / sys.argv[1]
    so = set(sys.argv[2:])
    itens = json.loads((pasta / "itens.json").read_text(encoding="utf-8"))
    (pasta / "fotos").mkdir(exist_ok=True)
    for it in itens:
        if it.get("foto_pronta") or (so and it["codigo"] not in so):
            continue
        p = produto(it)
        roupa_k, roupa = gerar.escolher_roupa(p)
        prompt = gerar.montar_prompt(p, roupa)
        imgs = [config.MODELO, p.get("_ref") or (config.FOTOS / p["foto_peca"])]
        if not p.get("_ref") and gerar.usa_foto_em_uso(p):
            imgs.append(config.FOTOS / p["foto_em_uso"])
        saida = pasta / "fotos" / f"{it['codigo']}.png"
        for tentativa in range(2):
            try:
                gemini.gerar_imagem(prompt, imgs, saida); print("ok", it["codigo"], roupa_k); break
            except Exception as e:
                print("erro", it["codigo"], e); time.sleep(10)
