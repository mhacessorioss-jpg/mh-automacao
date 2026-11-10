"""Baixa bio e posts do perfil (para revisão). Salva em revisao/perfil.json e revisao/thumbs/."""
import json, requests
from . import config
from .instagram import _api
tok = config.IG_ACCESS_TOKEN
r = requests.get(_api(config.IG_USER_ID), params={"fields": "username,name,biography,website,followers_count,follows_count,media_count", "access_token": tok}, timeout=30).json()
posts, url = [], _api(f"{config.IG_USER_ID}/media")
params = {"fields": "id,caption,media_type,media_url,thumbnail_url,permalink,timestamp,like_count,comments_count", "limit": 100, "access_token": tok}
while url and len(posts) < 300:
    j = requests.get(url, params=params, timeout=60).json()
    posts += j.get("data", []); url = j.get("paging", {}).get("next"); params = None
pasta = config.RAIZ / "revisao" / "thumbs"; pasta.mkdir(parents=True, exist_ok=True)
for i, p in enumerate(posts):
    u = p.get("thumbnail_url") or p.get("media_url")
    if u:
        try: (pasta / f"{i:03d}.jpg").write_bytes(requests.get(u, timeout=60).content)
        except Exception as e: print("thumb", i, e)
(config.RAIZ / "revisao" / "perfil.json").write_text(json.dumps({"perfil": r, "posts": posts}, ensure_ascii=False, indent=1), encoding="utf-8")
print(r, len(posts))
