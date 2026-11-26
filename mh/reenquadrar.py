"""Refaz fotos de brinco em close da orelha. Uso: python -m mh.reenquadrar <lista.json>
lista.json: [{"foto": "caminho/da/foto.png", "ref": "caminho/ref_produto", "saida": "caminho/saida.png", "extra": "..."}]"""
import sys, json
from concurrent.futures import ThreadPoolExecutor
from . import config, gemini

PROMPT = ("Refaça esta foto de joalheria como um CLOSE MACRO DE PERFIL DA ORELHA da mesma modelo: a orelha ocupa boa parte da imagem, "
"aparecendo só parte da bochecha, da mandíbula e do cabelo castanho preso para trás; sem mostrar o rosto inteiro nem os olhos. "
"Mantenha a mesma pele, o mesmo cabelo e a mesma luz quente; fundo bege desfocado. "
"O brinco deve ser IDÊNTICO ao da segunda imagem (formato, cor, pedras e acabamento), em TAMANHO REAL em relação à orelha, preso no furo do lóbulo, "
"nítido, com sombra suave e reflexos naturais, sem aspecto de montagem. Se a segunda imagem for um TRIO (três brincos diferentes), "
"use os três na MESMA orelha, cada um em um furo do lóbulo/parte baixa da orelha, lado a lado, cada peça uma única vez. "
"Sem textos. Formato vertical 3:4.")

def um(it):
    try:
        imgs = [config.RAIZ / it["foto"]] + ([config.RAIZ / it["ref"]] if it.get("ref") else [])
        s = config.RAIZ / it["saida"]; s.parent.mkdir(parents=True, exist_ok=True)
        gemini.gerar_imagem(PROMPT + (" " + it["extra"] if it.get("extra") else ""), imgs, s)
        print("ok", it["saida"], flush=True)
    except Exception as e:
        print("erro", it["saida"], e, flush=True)

if __name__ == "__main__":
    lista = json.load(open(config.RAIZ / sys.argv[1], encoding="utf-8"))
    with ThreadPoolExecutor(4) as ex: list(ex.map(um, lista))
