# MH Acessórios: automação de posts no Instagram

Todo dia o robô:
1. escolhe a próxima peça do catálogo, alternando as categorias;
2. gera a foto da peça na **modelo oficial da MH** com o Gemini;
3. aplica o selo da marca e escreve a legenda no tom da MH, **sem preço**;
4. abre um **pedido de aprovação** (uma *Issue*), que você vê no app GitHub do celular;
5. quando você aprova, **publica no Instagram**.

## No dia a dia (pelo celular)
Instale o app **GitHub** e abra a aba *Issues* do repositório `mh-automacao`. Cada post aparece como "📸 Aprovar post: …".

| Você quer… | Faça |
|---|---|
| Publicar | adicione a etiqueta **aprovado** |
| Outra imagem | adicione a etiqueta **refazer** |
| Mudar a legenda | edite o texto da issue (entre as marcações de LEGENDA) e depois aprove |
| Pular a peça | feche a issue |
| Gerar um post agora | aba *Actions* → "1 · Gerar post do dia" → *Run workflow* (pode informar um código) |

## Configuração (uma vez só)
Em **Settings → Secrets and variables → Actions → New repository secret**:

| Segredo | Onde conseguir |
|---|---|
| `GEMINI_API_KEY` | aistudio.google.com → *Get API key* (precisa de faturamento ativo para gerar imagens) |
| `IG_USER_ID` | ID da conta profissional do Instagram (passo a passo da Meta) |
| `IG_ACCESS_TOKEN` | Token de longa duração da Meta com `instagram_content_publish` |

Opcional, em *Variables*: `GEMINI_IMAGE_MODEL`, `GEMINI_TEXT_MODEL`, `GRAPH_HOST` (`graph.instagram.com` se usar o "Login do Instagram") e `GRAPH_VERSION`.

Em **Settings → Actions → General → Workflow permissions**, marque **Read and write permissions**.

## Onde ajustar sem mexer em código
- `config/prompts.json`: como a modelo usa cada tipo de peça (pescoço, orelha, mão…)
- `config/marca.json`: tom de voz, chamada, hashtags e palavras proibidas
- `marca/modelo_oficial.png`: a foto de referência da modelo

## Peças novas
Coloque as fotos em `fotos/` (`CODIGO_01.jpg` = peça em uso, `CODIGO_02.jpg` = fundo branco), atualize a planilha e rode `python scripts/gerar_catalogo.py <planilha.xlsx>` no seu computador (a planilha tem preços e **não** deve subir para o repositório público). Ou peça para o Claude fazer isso.

Ficam fora da fila automática as peças infantis ou licenciadas, as peças sem foto, as que estão com cor pendente e as variações de tamanho repetidas (veja a coluna `motivo_inativo` em `catalogo/produtos.csv`).
