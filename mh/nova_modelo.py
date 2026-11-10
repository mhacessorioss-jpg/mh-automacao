"""Gera opções de nova modelo oficial no estilo das referências da marca (marca/estilo/).

Uso: python -m mh.nova_modelo
Salva marca/candidatas/modelo_opcao_1..3.png
"""
from . import config, gemini

BASE = ("Crie um RETRATO fotorrealista de uma NOVA modelo (uma pessoa inventada, que não é nenhuma das mulheres das imagens de referência). "
        "Use as imagens de referência APENAS para copiar o ESTILO: luz dourada quente de fim de tarde, pele iluminada e bronzeada com brilho saudável, "
        "maquiagem glam suave (pele glow, cílios marcados, sobrancelhas definidas, batom nude rosado brilhante), paleta bege/dourada, fundo creme desfocado. "
        "Enquadramento: retrato do peito para cima, rosto de três quartos, olhar elegante, sorriso leve, ombros à mostra com blusa off-white de alcinha ou decote V. "
        "Ela NÃO usa NENHUMA joia (nada nas orelhas, pescoço, mãos). Orelhas visíveis (cabelo atrás de uma orelha). Formato vertical 4:5, sem texto.")

OPCOES = [
    "Mulher brasileira de ~28 anos, pele morena dourada, cabelo castanho longo e ondulado com luzes mel/caramelo, olhos castanhos.",
    "Mulher brasileira de ~30 anos, pele clara bronzeada, cabelo castanho-claro liso e longo com mechas loiras iluminadas, olhos castanho-esverdeados.",
    "Mulher brasileira de ~27 anos, pele morena, cabelo castanho-escuro volumoso com ondas largas e reflexos chocolate, olhos castanho-escuros.",
]

if __name__ == "__main__":
    pasta = config.RAIZ / "marca" / "candidatas"; pasta.mkdir(exist_ok=True)
    refs = sorted((config.RAIZ / "marca" / "estilo").glob("ref_estilo_*.png"))
    for i, desc in enumerate(OPCOES, 1):
        try:
            gemini.gerar_imagem(BASE + " A modelo: " + desc, refs, pasta / f"modelo_opcao_{i}.png"); print("ok", i)
        except Exception as e:
            print("erro", i, e)
