"""Etapa 3: publica no Instagram o post da issue aprovada.

Uso: python -m mh.publicar <numero_da_issue>
A legenda publicada é a que está na issue (se você editou, vale a versão editada).
"""
import json, sys
from . import config, estado, github, instagram


def main(n: int):
    iss = github.ler_issue(n)
    cod, leg = github.extrair(iss["body"])
    est = estado.ler()
    if cod in est["postados"]:
        github.comentar(n, "Esta peça já foi publicada antes; nada foi feito.")
        return
    info = json.loads((config.FILA / cod / "info.json").read_text(encoding="utf-8"))
    url = config.url_publica(f"fila/{cod}/post.jpg") + f"?v={info['versao']}"
    try:
        link = instagram.publicar_foto(url, leg)
    except Exception as e:
        github.comentar(n, f"⚠️ Não consegui publicar: `{e}`\n\nTire e coloque a etiqueta **aprovado** de novo para tentar outra vez.")
        github.tirar_etiqueta(n, "aprovado")
        raise
    est["postados"].append(cod)
    est["em_aprovacao"].pop(cod, None)
    est.setdefault("links", {})[cod] = link
    estado.salvar(est)
    github.comentar(n, f"✅ Publicado no Instagram: {link}")
    github.fechar(n)


if __name__ == "__main__":
    main(int(sys.argv[1]))
