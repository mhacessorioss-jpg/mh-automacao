"""Baixa fotos e nomes dos produtos de um pedido Febijus (páginas públicas).
Uso: python -m mh.baixar_febijus campanhas/<pasta>   (lê <pasta>/pedido.txt com linhas CODIGO:ID-VAR)"""
import json, re, sys, html
import requests
from . import config
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
pasta = config.RAIZ / sys.argv[1]
saida = config.RAIZ / "fotos"
info = {}
for linha in (pasta / "pedido.txt").read_text().split():
    cod, ids = linha.split(":")
    url = f"https://www.febijus.com.br/produto/p-{ids}"
    try:
        h = requests.get(url, headers=UA, timeout=60).text
    except Exception as e:
        print("ERRO", cod, e); continue
    t = re.search(r'<meta property="og:title" content="([^"]+)"', h) or re.search(r"<title>([^<]+)</title>", h)
    titulo = html.unescape(t.group(1)).strip() if t else cod
    imgs = list(dict.fromkeys(re.findall(r'https?://febijus\.bwimg\.com\.br/febijus/produtos/[^"\' )]+?\.(?:jpg|jpeg|png|webp)', h, re.I)))
    if not imgs:
        print("SEM FOTO", cod); continue
    base = re.sub(r"-\d+\.\d+\.\w+$", "", imgs[0].split("/produtos/")[1])
    principais = [u for u in imgs if u.split("/produtos/")[1].startswith(base[:25])][:3] or imgs[:1]
    arqs = []
    for i, u in enumerate(principais, 1):
        dst = saida / f"{cod}_0{i}.jpg"
        dst.write_bytes(requests.get(u, headers=UA, timeout=60).content); arqs.append(dst.name)
    info[cod] = {"titulo": titulo, "fotos": arqs, "url": url}
    print("ok", cod, len(arqs), titulo[:70])
(pasta / "produtos.json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
