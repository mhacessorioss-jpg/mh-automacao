"""Mostra o status dos convites de colaboração de um post. Uso: python -m mh.colaboradores <shortcode>"""
import sys, requests
from . import config
from .instagram import _api
tok = config.IG_ACCESS_TOKEN
code = sys.argv[1]
url, params = _api(f"{config.IG_USER_ID}/media"), {"fields": "id,permalink", "limit": 50, "access_token": tok}
mid = next(m["id"] for m in requests.get(url, params=params, timeout=30).json()["data"] if code in m.get("permalink", ""))
print(requests.get(_api(f"{mid}/collaborators"), params={"access_token": tok}, timeout=30).json())
