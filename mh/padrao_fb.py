"""Recria a foto de uso do brinco no padrão da FB, trocando só a pessoa pela modelo MH.
Uso: python -m mh.padrao_fb <lista.json>  — itens: {"base": foto FB de uso, "ref": foto do produto, "saida": png}"""
import sys, json
from concurrent.futures import ThreadPoolExecutor
from . import config, gemini

MODELO = "marca/modelo_oficial_sem_joias.png"
PROMPT = ("Recrie a PRIMEIRA imagem mantendo EXATAMENTE a mesma composição: mesmo enquadramento, mesmo ângulo da cabeça, mesma distância da câmera, "
"mesma posição e o MESMO TAMANHO do brinco em relação à orelha, e o brinco idêntico (formato, cor, pedras, acabamento — confira na terceira imagem). "
"Troque SOMENTE a pessoa pela modelo da segunda imagem: mesmo tom de pele, cabelo castanho com luzes preso para trás, maquiagem natural com batom nude (sem batom vermelho). "
"Remova quaisquer outros brincos, piercings ou ear cuffs que não façam parte do produto. Fundo bege claro liso e luz suave e quente, como fotografia profissional de joalheria. "
"Sem textos, logos ou marcas d'água.")

def um(it):
    try:
        s = config.RAIZ / it["saida"]
        imgs = [config.RAIZ / it["base"], config.RAIZ / MODELO] + ([config.RAIZ / it["ref"]] if it.get("ref") else [])
        gemini.gerar_imagem(PROMPT + (" " + it["extra"] if it.get("extra") else ""), imgs, s)
        print("ok", it["saida"], flush=True)
    except Exception as e:
        print("erro", it["saida"], e, flush=True)

if __name__ == "__main__":
    lista = json.load(open(config.RAIZ / sys.argv[1], encoding="utf-8"))
    with ThreadPoolExecutor(4) as ex: list(ex.map(um, lista))
