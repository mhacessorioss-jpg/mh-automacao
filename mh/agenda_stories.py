"""Publica os Stories da agenda cujo horário (Brasília) já chegou.

Uso: python -m mh.agenda_stories campanhas/black-friday
Lê <campanha>/agenda.json: [{"codigo","arquivo","horario":"AAAA-MM-DD HH:MM","publicado":null}]
"""
import json, sys
from datetime import datetime, timedelta, timezone
from . import config, instagram

BRT = timezone(timedelta(hours=-3))

if __name__ == "__main__":
    pasta = config.RAIZ / sys.argv[1]
    arq = pasta / "agenda.json"
    agenda = json.loads(arq.read_text(encoding="utf-8"))
    agora = datetime.now(BRT)
    for it in agenda:
        if it.get("publicado"):
            continue
        quando = datetime.strptime(it["horario"], "%Y-%m-%d %H:%M").replace(tzinfo=BRT)
        if quando <= agora:
            url = config.url_publica(f"{sys.argv[1]}/{it['arquivo']}") + f"?v={int(agora.timestamp())}"
            try:
                it["publicado"] = instagram.publicar_foto(url, story=True)
                print("Story publicado:", it["codigo"], it["publicado"])
            except Exception as e:
                print("ERRO", it["codigo"], e)
    arq.write_text(json.dumps(agenda, ensure_ascii=False, indent=1), encoding="utf-8")
