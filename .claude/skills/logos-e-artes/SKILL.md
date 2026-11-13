---
name: logos-e-artes
description: Use ao criar logo, ícone de app, banner, post, flyer ou qualquer arte para os apps e marcas do Samuel. Define quando desenhar em vetor (SVG) e quando gerar imagem por IA, e o checklist de qualidade.
---

# Logos e artes com qualidade profissional

## 1. Escolha o caminho certo
| Pedido | Caminho |
|---|---|
| Logo, ícone de app, selo, tipografia, banner com texto | **Vetor (SVG)** desenhado em código → exportar PNG. Texto sai perfeito e a imagem é nítida em qualquer tamanho. |
| Foto realista, ilustração rica, cenário, produto em ambiente | **IA de imagem** (`scripts/gerar_imagem.py` ou conector Adobe Firefly/Express, se disponível). |
| Arte final com foto + texto | Gerar a foto por IA **sem texto** e montar o texto por cima em SVG/HTML. A IA erra letras; o código não. |

Nunca deixe a IA escrever o texto da arte (nome da marca, preços, WhatsApp).

## 2. Logo em SVG (padrão)
1. Faça 3 conceitos diferentes antes de escolher: símbolo + nome, monograma (ex.: "SB") e só tipografia.
2. Regras: formas simples e geométricas, no máximo 2 ou 3 cores, legível em 48 px, funcionando em fundo claro e escuro.
3. Tipografia: use fontes de `canvas-design/canvas-fonts` (licença OFL) e **converta o texto em contorno** ou embuta a fonte, para não depender da fonte instalada.
4. Paleta: respeite a do projeto (ex.: preto e dourado, palha e dourado, vintage com pátina). Use `theme-factory` para combinações.
5. Exporte:
   ```bash
   rsvg-convert -w 1024 -h 1024 logo.svg -o logo-1024.png      # mestre
   rsvg-convert -w 512  -h 512  logo.svg -o icone-play-512.png # Play Store
   rsvg-convert -w 192  -h 192  logo.svg -o icon-192.png       # PWA
   ```
6. Ícone de app: símbolo centralizado com margem de segurança (~20%), sem texto pequeno, fundo sólido.

## 3. Imagem por IA (`scripts/gerar_imagem.py`)
- Precisa da chave em variável de ambiente (nunca no repositório): `IMAGE_API_KEY`.
  Opcional: `IMAGE_API_BASE` (padrão OpenAI) e `IMAGE_MODEL` (confira o nome do modelo atual na documentação do provedor).
- Uso: `python3 .claude/skills/logos-e-artes/scripts/gerar_imagem.py "prompt" saida.png --size 1024x1024`
- Prompt bom: assunto + estilo + luz + enquadramento + paleta + "sem texto, sem letras, sem marca d'água".
  Ex.: `"mesa de madeira antiga restaurada com pátina dourada, luz suave de janela, foto de produto, fundo neutro bege, sem texto"`.
- Gere 2 a 4 variações e escolha. Recorte fundo e ajuste tamanho com `convert` (ImageMagick).

## 4. Banners e posts
- Tamanhos: post 1080×1080, story/status 1080×1920, banner Play 1024×500, capa 1200×630.
- Monte em HTML/SVG: foto de fundo + faixa de contraste + título curto + chamada (WhatsApp) + logo.
- Visual limpo e de vendas: 1 mensagem principal, no máximo 2 fontes, contraste alto, nada poluído.
- **Nunca remova logos ou marcas** que o Samuel enviou.

## 5. Checklist antes de entregar
- Ortografia conferida letra por letra (nomes, preços, telefone).
- Conferir a imagem final abrindo o PNG (não só o código).
- Legível no celular em tamanho real.
- Entregar SVG + PNG e dizer qual arquivo usar onde.
- Não copiar logos, personagens ou artes de outras marcas.
