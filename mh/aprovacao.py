"""Etapa 2: abre (ou atualiza) a issue de aprovação com a imagem e a legenda.

Uso:
  python -m mh.aprovacao abrir COL12362
  python -m mh.aprovacao refeito 12      # após 'refazer', mostra a nova imagem na issue 12
  python -m mh.aprovacao descartar 12    # issue fechada sem aprovar
"""
import json, sys
from . import config, estado, github


def _img_url(cod):
    info = json.loads((config.FILA / cod / "info.json").read_text(encoding="utf-8"))
    return config.url_publica(f"fila/{cod}/post.jpg") + f"?v={info['versao']}"


def abrir(cod):
    p = estado.proximo_produto(cod)
    leg = (config.FILA / cod / "legenda.txt").read_text(encoding="utf-8")
    n = github.abrir_issue(p, _img_url(cod), leg)
    est = estado.ler(); est["em_aprovacao"][cod] = n; estado.salvar(est)
    print(f"Issue #{n} aberta para {cod}")


def refeito(n):
    iss = github.ler_issue(n)
    cod, leg = github.extrair(iss["body"])
    p = estado.proximo_produto(cod)
    github.atualizar_corpo(n, github.corpo_issue(p, _img_url(cod), leg))
    github.tirar_etiqueta(n, "refazer")
    github.comentar(n, f"🔄 Nova imagem gerada:\n\n![nova]({_img_url(cod)})")


def descartar(n):
    iss = github.ler_issue(n)
    cod, _ = github.extrair(iss["body"])
    est = estado.ler()
    est["em_aprovacao"].pop(cod, None)
    est.setdefault("descartados", [])
    if cod not in est["descartados"] and cod not in est["postados"]:
        est["descartados"].append(cod)
        est["postados"].append(cod)  # não volta para a fila automática
    estado.salvar(est)
    print(f"{cod} pulado.")


if __name__ == "__main__":
    acao, arg = sys.argv[1], sys.argv[2]
    {"abrir": lambda: abrir(arg), "refeito": lambda: refeito(int(arg)),
     "codigo": lambda: print(github.extrair(github.ler_issue(int(arg))["body"])[0]),
     "descartar": lambda: descartar(int(arg))}[acao]()
