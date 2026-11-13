---
name: edicao-de-imagens
description: Use quando o Samuel enviar fotos ou imagens para editar: remover fundo, recortar no tamanho de post/story/Play Store, melhorar cor e luz, colocar logo/marca d'água, moldura, comprimir ou editar várias de uma vez (lote).
---

# Edição de imagens profissional

Ferramenta principal: `scripts/editar.py` (Pillow). Rode `python3 scripts/editar.py -h` para ver tudo.
Todo comando aceita **um arquivo ou uma pasta** (pasta = edita todas em lote).

## Regras
1. **Nunca edite o original.** Trabalhe numa cópia e entregue em arquivo novo (`nome-editado.jpg`).
2. **Nunca remova logos ou marcas** que estejam na imagem, a menos que o Samuel peça.
3. Abra e **olhe o resultado** antes de entregar. Compare antes e depois lado a lado
   (`convert antes.jpg depois.jpg +append comparar.jpg`).
4. Texto em cima de imagem: monte em SVG ou HTML (skill `logos-e-artes`) e confira a ortografia letra por letra.
5. Fotos com rosto de pessoas: só ajustes de luz e cor. Não mude feições.

## Receitas rápidas
| Pedido | Comando |
|---|---|
| Post do Instagram/WhatsApp | `editar.py tamanho foto.jpg post.jpg --preset post` (`post-retrato` = 1080×1350) |
| Story/status | `editar.py tamanho foto.jpg story.jpg --preset story` |
| Caber sem cortar | adicione `--modo caber --fundo "#0B0B0B"` |
| Foto escura ou sem vida | `editar.py ajustar foto.jpg ok.jpg --auto --brilho 1.08 --saturacao 1.1` |
| Tom mais quente (madeira, vintage) | `--temperatura 10` (negativo esfria) |
| Mais nítida | `--nitidez 1.4` |
| Logo no canto | `editar.py marca foto.jpg ok.jpg --logo logo.png --posicao inf-dir --largura 0.2` |
| Remover fundo (PNG transparente) | `editar.py fundo foto.jpg recorte.png` |
| Fundo branco com sombra | `editar.py fundo foto.jpg ok.jpg --cor "#ffffff" --sombra` |
| Moldura dourada vintage | `editar.py moldura foto.jpg ok.png --cor "#C9A24A" --fundo "#0B0B0B"` |
| Deixar leve para site/app | `editar.py comprimir foto.jpg leve --formato webp --max-kb 250` |
| Ver tamanho e peso | `editar.py info pasta/` |

Remover fundo usa `rembg` (`pip install --break-system-packages "rembg[cpu]"`). Se não instalar ou o recorte
ficar ruim (cabelo, vidro, renda), use o **conector Adobe**, se disponível: `image_remove_background`,
`image_select_subject` e `image_fill_area` (apagar objeto), `image_generative_expand` (aumentar a foto para
caber no formato sem cortar) e `image_vectorize` (logo em vetor).

## Fluxo padrão
1. `info`: veja o tamanho e o estado da foto.
2. Corrija a luz e a cor (`ajustar`), sem exagerar. A cor da peça tem que ser fiel à real.
3. Recorte no formato de destino (`tamanho`).
4. Aplique marca ou moldura, se pedido.
5. Comprima para o destino: WhatsApp e Instagram em JPG, com cerca de 1080 px; site e app em WebP.
6. Mostre o antes e depois e entregue os arquivos.

## Tamanhos de referência
Post 1080×1080 · Retrato 1080×1350 · Story 1080×1920 · Capa/link 1200×630 ·
Banner Play 1024×500 · Ícone Play 512×512 · PWA 192/512 · Produto 1600×1600 · A4 300 dpi 2480×3508.
