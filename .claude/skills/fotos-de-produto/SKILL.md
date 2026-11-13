---
name: fotos-de-produto
description: Use para preparar fotos de peças, móveis restaurados, roupas e prêmios para vender (vitrine, catálogo, lives, rifas, grupo VIP): padronizar fundo, luz e tamanho, montar catálogo e cards de preço.
---

# Fotos de produto que vendem

Usa `../edicao-de-imagens/scripts/editar.py` para o trabalho pesado.

## Padrão de vitrine
1. **Cor fiel à peça**: madeira, pátina e tecido precisam parecer como são ao vivo. Ajuste a luz, não invente cor.
2. **Fundo limpo e igual em todas** as fotos do mesmo catálogo: branco (`#ffffff`), off-white (`#F4EFE6`) ou preto (`#0B0B0B`) para peças douradas.
3. **Peça centralizada**, ocupando de 75% a 85% do quadro, com sombra suave no chão.
4. **Tamanho único**: 1600×1600 para a loja e 1080×1080 para WhatsApp e Instagram.
5. Logo da loja pequena no canto, sempre na mesma posição.

```bash
E=.claude/skills/edicao-de-imagens/scripts/editar.py
python3 $E ajustar  originais/ etapa1/ --auto --nitidez 1.2
python3 $E fundo    etapa1/    etapa2/ --cor "#F4EFE6" --sombra
python3 $E tamanho  etapa2/    etapa3/ --preset produto --modo caber --fundo "#F4EFE6"
python3 $E marca    etapa3/    final/  --logo logo.png --largura 0.16 --opacidade 0.85
python3 $E comprimir final/    web/    --formato webp --max-kb 250
```

## Móveis grandes e peças com fundo difícil
- Se remover o fundo cortar pés, puxadores ou detalhes vazados, **não remova**: só ajuste a luz e recorte o enquadramento.
- Para limpar objetos no fundo (fio, caixa, parede manchada), use o conector Adobe (`image_fill_area`), se disponível.
- Para restauro, faça **antes e depois** lado a lado, do mesmo ângulo e com a mesma luz.

## Card de venda (preço, rifa, live)
Monte em SVG ou HTML (skill `logos-e-artes`): foto + nome da peça + preço ou número da rifa + WhatsApp + logo.
- Uma informação principal, contraste alto, no máximo 2 fontes.
- Preço no formato `R$ 1.250,00`. Confira a ortografia de tudo antes de entregar.

## Catálogo (folha com várias peças)
Grade de 2×3 ou 3×3 em A4 (2480×3508) ou story, com o mesmo fundo, nome e preço embaixo de cada foto
e a logo no rodapé. Exporte em PDF para imprimir e em JPG para o WhatsApp.

## Entrega
Entregue as fotos finais, as versões web e um antes e depois de 1 foto, para o Samuel aprovar o padrão antes do lote inteiro.
