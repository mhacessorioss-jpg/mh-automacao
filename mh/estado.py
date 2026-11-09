"""Controle do que já foi postado e do que está aguardando aprovação."""
import csv, json
from . import config

ORDEM_CATEGORIAS = ["brinco", "colar", "anel", "conjunto", "pulseira", "brinco", "colar", "tornozeleira", "piercing"]


def ler():
    return json.loads(config.ESTADO.read_text(encoding="utf-8"))


def salvar(est):
    config.ESTADO.write_text(json.dumps(est, ensure_ascii=False, indent=2), encoding="utf-8")


def catalogo():
    with open(config.CATALOGO, encoding="utf-8") as f:
        return [r for r in csv.DictReader(f)]


def proximo_produto(codigo_forcado: str | None = None):
    """Escolhe a próxima peça: alterna categorias e nunca repete o que já foi postado ou está em aprovação."""
    est = ler()
    prods = catalogo()
    if codigo_forcado:
        return next(p for p in prods if p["codigo"] == codigo_forcado)
    usados = set(est["postados"]) | set(est["em_aprovacao"])
    livres = [p for p in prods if p["ativo"] == "sim" and p["codigo"] not in usados]
    if not livres:
        return None
    n = len(est["postados"]) + len(est["em_aprovacao"])
    for i in range(len(ORDEM_CATEGORIAS)):
        cat = ORDEM_CATEGORIAS[(n + i) % len(ORDEM_CATEGORIAS)]
        cand = [p for p in livres if p["categoria"] == cat]
        if cand:
            return cand[0]
    return livres[0]
