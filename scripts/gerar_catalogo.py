"""Gera catalogo/produtos.csv a partir da planilha de preparação Shopee.

Uso: python scripts/gerar_catalogo.py scripts/planilha_origem.xlsx
Rode de novo sempre que a planilha mudar (peças novas, estoque, status).
Preço e custo NÃO entram no catálogo (o repositório pode ser público).
"""
import csv, re, sys
from pathlib import Path
import openpyxl

RAIZ = Path(__file__).resolve().parent.parent
FOTOS = RAIZ / "fotos"

CATEGORIAS = {
    "Anéis": "anel", "Brincos": "brinco", "Colares": "colar", "Pulseiras": "pulseira",
    "Tornozeleiras": "tornozeleira", "Conjuntos": "conjunto", "Piercings": "piercing",
}

# Fora da automação: peças infantis (não combinam com a modelo adulta),
# personagens licenciados e peças sem foto ou com cor a conferir.
EXCLUIR_PALAVRAS = ["infantil", "minnie"]
# Mesma peça em outro tamanho: posta só uma vez.
DUPLICADOS = {"AN3696-4": "mesma peça de AN3696-3 (outro tamanho)"}


def categoria(cod, cat_planilha):
    if cat_planilha in CATEGORIAS:
        return CATEGORIAS[cat_planilha]
    pref = re.match(r"[A-Z]+", cod).group(0)
    return {"AN": "anel", "BRI": "brinco", "COL": "colar", "PUL": "pulseira", "TO": "tornozeleira",
            "CEB": "conjunto", "PG": "piercing"}.get(pref, "outro")


def nome_vitrine(desc):
    n = desc
    n = re.sub(r"\s*-\s*(Ouro|Prata|Branco|Ouro-Preto|Ouro-Cristal|Ouro-C)\b.*$", "", n)
    n = re.sub(r"\s*-\s*\d+\s*$", "", n)
    n = re.sub(r"(A[cç]o Inoxidavel |A[cç]o Inoxidável |A[cç]o Inox )", "", n, flags=re.I)
    n = re.sub(r"Folhead[oa] a Ouro 18[kK]( e Prata)?\s*", "", n)
    n = re.sub(r"Semi Joia\s*", "", n)
    n = re.sub(r"Inspira[cç][aã]o Vg\.?\s*", "", n, flags=re.I)  # nunca citar marca de terceiros
    fix = {"Coracao": "Coração", "Coracoes": "Corações", "Organico": "Orgânico", "Zirconia": "Zircônia",
           "Perola": "Pérola", "Tres": "Três", "Triangulo": "Triângulo", "Circulo": "Círculo",
           "Espirito": "Espírito", "Aco": "Aço", "Ovais": "Ovais", "Colorido": "Coloridos"}
    for a, b in fix.items():
        n = re.sub(rf"\b{a}\b", b, n)
    n = re.sub(r"^Anel de ", "Anel ", n)
    n = {"Colar Dupla": "Colar Pingente Duplo", "Choker Verde": "Choker Trevos Verdes",
         "Trio de Brinco Vazado": "Trio de Brinco Argolas Trevo Vazado",
         "Trio de Brinco Verde e Esfera Texturizado": "Trio de Brinco Trevo Verde e Esfera Texturizada",
         "Anel Resinado Com Ponto de Luz": "Anel Resina Branca Com Ponto de Luz"}.get(n.strip(), n)
    return re.sub(r"\s+", " ", n).strip()


def material(desc, acab):
    acab = (acab or "").upper()
    inox = bool(re.search(r"a[cç]o inox", desc, re.I))
    if acab.startswith("PRATEADO"):
        return "Acabamento prateado" + (" · aço inoxidável" if inox else "")
    return ("Aço inoxidável folheado a ouro 18k" if inox else "Folheado a ouro 18k")


def foto_ref(cod):
    """Prefere a foto em fundo branco (_02); se não houver, usa a _01."""
    fotos = sorted(FOTOS.glob(f"{cod}_0*.jpg"))
    if not fotos:
        return "", ""
    p02 = FOTOS / f"{cod}_02.jpg"
    p01 = FOTOS / f"{cod}_01.jpg"
    principal = p02 if p02.exists() else fotos[0]
    worn = p01.name if p01.exists() and p01 != principal else ""
    return principal.name, worn


def main(xlsx):
    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    ws = wb["Shopee"]
    linhas = list(ws.iter_rows(values_only=True))
    cab = [str(c or "") for c in linhas[3]]
    idx = {c: i for i, c in enumerate(cab)}
    saida = []
    for r in linhas[4:]:
        cod = r[idx["CÓDIGO"]]
        if not cod:
            continue
        cod = str(cod).strip()
        desc = str(r[idx["DESCRIÇÃO"]] or "")
        status = str(r[idx["STATUS PARA SHOPEE"]] or "")
        acab = str(r[idx["COR/ACABAMENTO"]] or "")
        estoque = r[idx["ESTOQUE DISPONÍVEL"]] or 0
        principal, worn = foto_ref(cod)
        motivo = ""
        if not principal:
            motivo = "sem foto"
        elif "CONFERIR" in status.upper() or "SEM FOTO" in status.upper():
            motivo = "status: " + status
        elif acab.upper().startswith("PENDENTE"):
            motivo = "cor pendente de conferência"
        elif any(p in desc.lower() for p in EXCLUIR_PALAVRAS):
            motivo = "peça infantil/licenciada"
        elif cod in DUPLICADOS:
            motivo = DUPLICADOS[cod]
        elif int(estoque) <= 0:
            motivo = "sem estoque"
        saida.append({
            "codigo": cod,
            "nome_vitrine": nome_vitrine(desc),
            "categoria": categoria(cod, str(r[idx["CATEGORIA"]] or "")),
            "cor": "prateado" if acab.upper().startswith("PRATEADO") else "dourado",
            "material": material(desc, acab),
            "descricao_fornecedor": desc,
            "foto_peca": principal,
            "foto_em_uso": worn,
            "ativo": "nao" if motivo else "sim",
            "motivo_inativo": motivo,
        })
    out = RAIZ / "catalogo" / "produtos.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(saida[0].keys()))
        w.writeheader(); w.writerows(saida)
    ativos = sum(1 for s in saida if s["ativo"] == "sim")
    print(f"{len(saida)} produtos no catálogo, {ativos} ativos para postagem -> {out}")


if __name__ == "__main__":
    main(sys.argv[1])
