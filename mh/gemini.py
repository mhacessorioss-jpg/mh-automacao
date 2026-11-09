"""Chamadas à API do Gemini (imagem e texto)."""
import base64, time
from pathlib import Path
import requests
from . import config

URL = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"


def _img_part(path: Path):
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return {"inline_data": {"mime_type": mime, "data": base64.b64encode(path.read_bytes()).decode()}}


def _post(modelo, corpo, tentativas=3):
    for i in range(tentativas):
        r = requests.post(URL.format(modelo=modelo), json=corpo, timeout=180,
                          headers={"x-goog-api-key": config.GEMINI_API_KEY})
        if r.status_code in (429, 500, 503) and i < tentativas - 1:
            time.sleep(20 * (i + 1)); continue
        if not r.ok:
            raise RuntimeError(f"Gemini {r.status_code}: {r.text[:500]}")
        return r.json()


def gerar_imagem(prompt: str, imagens: list[Path], saida: Path) -> Path:
    corpo = {
        "contents": [{"parts": [{"text": prompt}] + [_img_part(p) for p in imagens]}],
        "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "4:5"}},
    }
    resp = _post(config.GEMINI_IMAGE_MODEL, corpo)
    for cand in resp.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            dado = part.get("inlineData") or part.get("inline_data")
            if dado and dado.get("data"):
                saida.write_bytes(base64.b64decode(dado["data"]))
                return saida
    motivo = resp.get("promptFeedback") or [c.get("finishReason") for c in resp.get("candidates", [])]
    raise RuntimeError(f"O Gemini não devolveu imagem. Motivo: {motivo}")


MODELOS_TEXTO_RESERVA = ["gemini-flash-latest", "gemini-2.5-flash", "gemini-2.0-flash"]


def gerar_texto(prompt: str) -> str:
    corpo = {"contents": [{"parts": [{"text": prompt}]}],
             "generationConfig": {"temperature": 0.9, "maxOutputTokens": 2048,
                                  "thinkingConfig": {"thinkingBudget": 0}}}
    ultimo = None
    for modelo in [config.GEMINI_TEXT_MODEL] + MODELOS_TEXTO_RESERVA:
        try:
            resp = _post(modelo, corpo, tentativas=1)
            break
        except RuntimeError as e:  # modelo inexistente/desativado: tenta o próximo
            ultimo = e
            if " 404" not in str(e) and " 400" not in str(e):
                raise
    else:
        raise ultimo
    partes = resp["candidates"][0]["content"]["parts"]
    return "".join(p.get("text", "") for p in partes).strip()
