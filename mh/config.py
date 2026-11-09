import json, os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FOTOS = RAIZ / "fotos"
FILA = RAIZ / "fila"
CATALOGO = RAIZ / "catalogo" / "produtos.csv"
ESTADO = RAIZ / "estado" / "estado.json"
MODELO = RAIZ / "marca" / "modelo_oficial_sem_joias.png"  # mesma modelo, sem joias (evita copiar brincos/colares)
SELO = RAIZ / "marca" / "selo_branco.png"

PROMPTS = json.loads((RAIZ / "config" / "prompts.json").read_text(encoding="utf-8"))
MARCA = json.loads((RAIZ / "config" / "marca.json").read_text(encoding="utf-8"))

# Segredos (no GitHub: Settings > Secrets and variables > Actions)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
IG_USER_ID = os.getenv("IG_USER_ID") or "17841401405850239"  # @mhacessorios_oficial (não é segredo)
IG_ACCESS_TOKEN = "".join(os.getenv("IG_ACCESS_TOKEN", "").split()).strip("\"'")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY", "")  # "usuario/repositorio", preenchido pelo Actions

# Ajustes (podem virar Variables no GitHub sem mexer no código)
GEMINI_IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL") or "gemini-2.5-flash-image"
GEMINI_TEXT_MODEL = os.getenv("GEMINI_TEXT_MODEL") or "gemini-flash-latest"
GRAPH_VERSION = os.getenv("GRAPH_VERSION") or "v24.0"
BRANCH = os.getenv("BRANCH") or "main"


def url_publica(caminho_relativo: str) -> str:
    """URL pública de um arquivo do repositório (o repositório precisa ser público)."""
    return f"https://raw.githubusercontent.com/{GITHUB_REPOSITORY}/{BRANCH}/{caminho_relativo}"
