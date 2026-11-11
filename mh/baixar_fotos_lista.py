"""Baixa fotos do CDN da Febijus a partir de <pasta>/fotos.txt (CODIGO|base|ts1,ts2)."""
import sys, requests
from PIL import Image
from io import BytesIO
from . import config
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/124 Safari/537.36", "Referer": "https://www.febijus.com.br/"}
pasta = config.RAIZ / sys.argv[1]
for l in (pasta / "fotos.txt").read_text().splitlines():
    cod, base, tss = l.split("|")
    for i, ts in enumerate(tss.split(","), 1):
        u = f"https://febijus.bwimg.com.br/febijus/produtos/{base}-{ts}"
        try:
            r = requests.get(u, headers=UA, timeout=60); r.raise_for_status()
            Image.open(BytesIO(r.content)).convert("RGB").save(config.RAIZ / "fotos" / f"{cod}_0{i}.jpg", quality=92)
            print("ok", cod, i)
        except Exception as e:
            print("ERRO", cod, i, e)
