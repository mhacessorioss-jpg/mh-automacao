"""Monta o post final 1080x1350 (4:5) com o selo da MH no canto."""
from pathlib import Path
from PIL import Image
from . import config

W, H = 1080, 1350


def montar(foto: Path, saida: Path, foco: float = 0.3, opacidade: float = 0.85) -> Path:
    img = Image.open(foto).convert("RGB")
    esc = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * esc), round(img.height * esc)), Image.LANCZOS)
    x = (img.width - W) // 2
    y = int((img.height - H) * foco)
    img = img.crop((x, y, x + W, y + H))

    selo = Image.open(config.SELO).convert("RGBA")
    selo = selo.crop(selo.getchannel("A").getbbox())
    selo.thumbnail((120, 120), Image.LANCZOS)
    selo.putalpha(selo.getchannel("A").point(lambda v: int(v * opacidade)))
    m = 48
    img.paste(selo, (W - selo.width - m, H - selo.height - m), selo)
    img.save(saida, "JPEG", quality=92)  # Instagram só aceita JPEG
    return saida
