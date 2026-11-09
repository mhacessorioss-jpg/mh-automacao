"""Monta a legenda: abertura criativa (Gemini) + estrutura fixa da marca."""
import random, re
from . import config, gemini

ABERTURAS_RESERVA = {
    "colar": ["Simples. Elegante. Essencial.", "Delicadeza que se nota.", "O detalhe que completa."],
    "brinco": ["Brilho que emoldura o rosto.", "Detalhe que transforma.", "Pequeno no tamanho, enorme no charme."],
    "anel": ["Movimento em forma de joia.", "Para mãos que contam histórias.", "Um gesto, muita presença."],
    "pulseira": ["No pulso, a elegância.", "Para usar sozinha ou em mix.", "Brilho na medida certa."],
    "tornozeleira": ["Leveza a cada passo.", "O detalhe do verão.", "Delicada do jeito certo."],
    "conjunto": ["Combinação perfeita.", "Tudo junto, tudo lindo.", "Pronta para presentear."],
    "piercing": ["Ousadia delicada.", "O detalhe da orelha.", "Brilho no lugar certo."],
}


def _abertura_ia(p: dict) -> tuple[str, str]:
    m = config.MARCA
    prompt = (
        "Você escreve legendas de Instagram para a MH Acessórios, marca de semijoias.\n"
        f"Tom de voz: {m['tom_de_voz']}\n"
        f"Nunca faça: {'; '.join(m['proibido'])}.\n\n"
        f"Peça: {p['nome_vitrine']} (categoria {p['categoria']}, cor {p['cor']}).\n"
        "Escreva EXATAMENTE 2 linhas, sem aspas e sem hashtags:\n"
        "Linha 1: frase de impacto curta (2 a 6 palavras), sem emoji.\n"
        "Linha 2: uma frase (até 18 palavras) que desperte desejo pela peça e diga quando usar."
    )
    linhas = [l.strip(" \"'") for l in gemini.gerar_texto(prompt).splitlines() if l.strip()]
    if len(linhas) < 2:
        raise ValueError("resposta incompleta")
    return linhas[0], linhas[1]


def _sem_proibidos(texto: str) -> bool:
    return not re.search(r"R\$|\d+[,.]\d{2}|van cleef|vivara|pandora|cartier|925", texto, re.I)


def montar(p: dict) -> str:
    m = config.MARCA
    abertura = linha = None
    if config.GEMINI_API_KEY:
        try:
            abertura, linha = _abertura_ia(p)
            if not _sem_proibidos(abertura + linha):
                abertura = linha = None
        except Exception as e:
            print("Aviso: legenda IA falhou, usando reserva:", e)
    if not abertura:
        abertura = random.choice(ABERTURAS_RESERVA.get(p["categoria"], ["Elegância em cada detalhe."]))
        linha = f"{p['nome_vitrine']}: a peça que faltava no seu porta-joias."

    tags = list(m["hashtags_fixas"]) + m["hashtags_por_categoria"].get(p["categoria"], [])
    tags.append(m["hashtag_material"].get(p["cor"], ""))
    return "\n".join([
        abertura,
        linha,
        "",
        f"✨ {p['nome_vitrine']}",
        m["linha_material"].format(material=p["material"]),
        m["linha_envio"],
        m["chamada"],
        "",
        " ".join(t for t in tags if t),
    ])
