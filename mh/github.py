"""Issues do GitHub usadas como 'caixa de aprovação' (dá para aprovar pelo app GitHub no celular)."""
import re
import requests
from . import config

API = "https://api.github.com"
ETIQUETAS = {"aprovação": "D4C5B0", "aprovado": "2DA44E", "refazer": "967E65"}


def _h():
    return {"Authorization": f"Bearer {config.GITHUB_TOKEN}", "Accept": "application/vnd.github+json"}


def _repo(caminho=""):
    return f"{API}/repos/{config.GITHUB_REPOSITORY}{caminho}"


def garantir_etiquetas():
    for nome, cor in ETIQUETAS.items():
        requests.post(_repo("/labels"), headers=_h(), json={"name": nome, "color": cor}, timeout=30)


def corpo_issue(p: dict, img_url: str, legenda: str) -> str:
    return f"""<!-- codigo:{p['codigo']} -->
![post]({img_url})

**Peça:** {p['nome_vitrine']} · `{p['codigo']}` · {p['categoria']}
**Referência do fornecedor:** ![ref]({config.url_publica('fotos/' + p['foto_peca'])})

### Legenda (pode editar este texto antes de aprovar)
<!-- LEGENDA -->
{legenda}
<!-- /LEGENDA -->

---
**O que fazer:**
- ✅ Publicar: adicione a etiqueta **aprovado**
- 🔄 Gerar outra imagem: adicione a etiqueta **refazer**
- ❌ Pular esta peça: feche a issue
"""


def abrir_issue(p: dict, img_url: str, legenda: str) -> int:
    garantir_etiquetas()
    r = requests.post(_repo("/issues"), headers=_h(), timeout=30, json={
        "title": f"📸 Aprovar post: {p['nome_vitrine']} ({p['codigo']})",
        "body": corpo_issue(p, img_url, legenda),
        "labels": ["aprovação"],
    })
    r.raise_for_status()
    return r.json()["number"]


def ler_issue(n: int) -> dict:
    r = requests.get(_repo(f"/issues/{n}"), headers=_h(), timeout=30)
    r.raise_for_status()
    return r.json()


def extrair(body: str) -> tuple[str, str]:
    cod = re.search(r"<!-- codigo:(.+?) -->", body).group(1).strip()
    m = re.search(r"<!-- LEGENDA -->\s*(.*?)\s*<!-- /LEGENDA -->", body, re.S)
    return cod, (m.group(1).strip() if m else "")


def comentar(n: int, texto: str):
    requests.post(_repo(f"/issues/{n}/comments"), headers=_h(), json={"body": texto}, timeout=30)


def atualizar_corpo(n: int, body: str):
    requests.patch(_repo(f"/issues/{n}"), headers=_h(), json={"body": body}, timeout=30)


def tirar_etiqueta(n: int, nome: str):
    requests.delete(_repo(f"/issues/{n}/labels/{nome}"), headers=_h(), timeout=30)


def fechar(n: int):
    requests.patch(_repo(f"/issues/{n}"), headers=_h(), json={"state": "closed"}, timeout=30)
