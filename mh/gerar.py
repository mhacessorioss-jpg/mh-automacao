"""Etapa 1: escolhe a peça, gera a foto na modelo oficial, aplica o selo e escreve a legenda.

Uso:
  python -m mh.gerar                    # próxima peça da fila
  python -m mh.gerar --codigo COL12362  # peça específica
  python -m mh.gerar --teste            # sem chave do Gemini: usa a foto do fornecedor (só para testar o fluxo)
O resultado fica em fila/<codigo>/ (post.jpg, legenda.txt, info.json).
"""
import argparse, json, random, shutil, time
from pathlib import Path
from . import config, estado, gemini, legenda, post


# A foto do fornecedor com a modelo DELES só é enviada se a peça não tiver foto em fundo branco.
# Assim o Gemini não mistura o rosto/batom da outra modelo com a modelo oficial da MH.
USAR_FOTO_EM_USO = False


def escolher_roupa(p):
    pr = config.PROMPTS
    opcoes = pr["roupas_por_categoria"].get(p["categoria"]) or pr["roupas_por_categoria"]["outro"]
    chave = random.choice(opcoes)
    return chave, pr["roupas"][chave]


def montar_prompt(p, roupa):
    pr = config.PROMPTS
    texto = pr["base"].format(nome=p["nome_vitrine"], cor=p["cor"], material=p["material"], roupa=roupa)
    texto += " " + pr["por_categoria"].get(p["categoria"], pr["por_categoria"]["outro"])
    if USAR_FOTO_EM_USO and p["foto_em_uso"]:
        texto += " " + pr["referencia_em_uso"]
    return texto


def gerar(p: dict, teste: bool = False) -> Path:
    pasta = config.FILA / p["codigo"]
    pasta.mkdir(parents=True, exist_ok=True)
    bruta = pasta / "gerada.png"
    imagens = [config.MODELO, config.FOTOS / p["foto_peca"]]
    if USAR_FOTO_EM_USO and p["foto_em_uso"]:
        imagens.append(config.FOTOS / p["foto_em_uso"])
    roupa_chave, roupa = escolher_roupa(p)
    prompt = montar_prompt(p, roupa)

    if teste or not config.GEMINI_API_KEY:
        print("MODO TESTE: sem Gemini, usando a foto do fornecedor no lugar da imagem gerada.")
        shutil.copy(config.FOTOS / (p["foto_em_uso"] or p["foto_peca"]), bruta)
    else:
        gemini.gerar_imagem(prompt, imagens, bruta)

    post.montar(bruta, pasta / "post.jpg")
    leg = legenda.montar(p)
    (pasta / "legenda.txt").write_text(leg, encoding="utf-8")
    (pasta / "info.json").write_text(json.dumps(
        {"produto": p, "roupa": roupa_chave, "prompt": prompt, "gerado_em": time.strftime("%Y-%m-%d %H:%M"),
         "versao": int(time.time())}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Post pronto: {pasta}")
    return pasta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--codigo")
    ap.add_argument("--teste", action="store_true")
    a = ap.parse_args()
    p = estado.proximo_produto(a.codigo)
    if not p:
        print("Todas as peças ativas já foram postadas. Atualize o catálogo para continuar.")
        return
    gerar(p, a.teste)
    # Registra para não ser escolhida de novo enquanto aguarda aprovação
    est = estado.ler()
    est["em_aprovacao"].setdefault(p["codigo"], None)
    estado.salvar(est)
    Path("ultimo_codigo.txt").write_text(p["codigo"])


if __name__ == "__main__":
    main()
