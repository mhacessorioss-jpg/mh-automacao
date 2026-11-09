"""Publicação no Instagram (API oficial da Meta, conta Profissional)."""
import os, time
import requests
from . import config

HOST = os.getenv("GRAPH_HOST") or "graph.facebook.com"  # use graph.instagram.com se o token for do "Login do Instagram"


def _api(caminho):
    return f"https://{HOST}/{config.GRAPH_VERSION}/{caminho}"


def _ok(r):
    if not r.ok:
        raise RuntimeError(f"Instagram {r.status_code}: {r.text[:500]}")
    return r.json()


def publicar_foto(image_url: str, legenda: str) -> str:
    tok = config.IG_ACCESS_TOKEN
    cont = _ok(requests.post(_api(f"{config.IG_USER_ID}/media"),
                             data={"image_url": image_url, "caption": legenda, "access_token": tok}, timeout=60))["id"]
    for _ in range(30):
        st = _ok(requests.get(_api(cont), params={"fields": "status_code", "access_token": tok}, timeout=30))
        if st.get("status_code") == "FINISHED":
            break
        if st.get("status_code") == "ERROR":
            raise RuntimeError(f"Instagram recusou a imagem: {st}")
        time.sleep(5)
    media = _ok(requests.post(_api(f"{config.IG_USER_ID}/media_publish"),
                              data={"creation_id": cont, "access_token": tok}, timeout=60))["id"]
    info = _ok(requests.get(_api(media), params={"fields": "permalink", "access_token": tok}, timeout=30))
    return info.get("permalink", f"https://www.instagram.com/ (id {media})")
