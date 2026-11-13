#!/usr/bin/env python3
"""Editor de imagens do padrão SB (Pillow; rembg opcional para remover fundo).

Comandos (todos aceitam arquivo OU pasta como entrada; pasta = lote):
  tamanho   ENTRADA SAIDA --preset post|story|capa|banner-play|icone-play|whatsapp|produto|a4 [--modo cobrir|caber] [--fundo #ffffff]
  ajustar   ENTRADA SAIDA [--auto] [--brilho 1.0] [--contraste 1.0] [--saturacao 1.0] [--nitidez 1.0] [--temperatura 0]
  marca     ENTRADA SAIDA --logo logo.png [--posicao inf-dir|inf-esq|sup-dir|sup-esq|centro] [--largura 0.22] [--opacidade 0.9]
  fundo     ENTRADA SAIDA [--cor #ffffff] [--sombra]          (remove o fundo; sem --cor deixa transparente)
  comprimir ENTRADA SAIDA [--formato webp|jpg|png] [--max-kb 300] [--max-lado 2048]
  moldura   ENTRADA SAIDA [--cor #C9A24A] [--espessura 0.03] [--fundo #0B0B0B] [--margem 0.06]
  info      ENTRADA
"""
import argparse
import io
import os
import sys

from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageOps

PRESETS = {
    "post": (1080, 1080), "post-retrato": (1080, 1350), "story": (1080, 1920),
    "capa": (1200, 630), "banner-play": (1024, 500), "icone-play": (512, 512),
    "whatsapp": (1080, 1080), "produto": (1600, 1600), "a4": (2480, 3508),
    "pwa-192": (192, 192), "pwa-512": (512, 512),
}
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff", ".heic"}


def cor(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def abrir(p):
    im = Image.open(p)
    im = ImageOps.exif_transpose(im)  # corrige foto de celular "deitada"
    return im.convert("RGBA")


def salvar(im, destino, qualidade=92):
    ext = os.path.splitext(destino)[1].lower()
    os.makedirs(os.path.dirname(os.path.abspath(destino)), exist_ok=True)
    if ext in (".jpg", ".jpeg"):
        fundo = Image.new("RGB", im.size, (255, 255, 255))
        fundo.paste(im, mask=im.split()[-1])
        fundo.save(destino, quality=qualidade, optimize=True, progressive=True, subsampling=0)
    elif ext == ".webp":
        im.save(destino, quality=qualidade, method=6)
    else:
        im.save(destino, optimize=True)
    print(destino)


def tamanho(im, a):
    w, h = PRESETS[a.preset]
    if a.modo == "cobrir":
        return ImageOps.fit(im, (w, h), Image.LANCZOS, centering=(0.5, 0.45))
    im2 = ImageOps.contain(im, (w, h), Image.LANCZOS)
    base = Image.new("RGBA", (w, h), cor(a.fundo) + (255,) if a.fundo else (0, 0, 0, 0))
    base.alpha_composite(im2, ((w - im2.width) // 2, (h - im2.height) // 2))
    return base


def ajustar(im, a):
    alfa = im.split()[-1]
    rgb = im.convert("RGB")
    if a.auto:
        rgb = ImageOps.autocontrast(rgb, cutoff=0.5)
    for fator, cls in ((a.brilho, ImageEnhance.Brightness), (a.contraste, ImageEnhance.Contrast),
                       (a.saturacao, ImageEnhance.Color), (a.nitidez, ImageEnhance.Sharpness)):
        if fator != 1.0:
            rgb = cls(rgb).enhance(fator)
    if a.temperatura:
        r, g, b = rgb.split()
        t = a.temperatura
        r = r.point(lambda v: max(0, min(255, v + t)))
        b = b.point(lambda v: max(0, min(255, v - t)))
        rgb = Image.merge("RGB", (r, g, b))
    out = rgb.convert("RGBA")
    out.putalpha(alfa)
    return out


def marca(im, a):
    logo = abrir(a.logo)
    lw = int(im.width * a.largura)
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    if a.opacidade < 1:
        logo.putalpha(logo.split()[-1].point(lambda v: int(v * a.opacidade)))
    m = int(min(im.size) * 0.04)
    pos = {
        "inf-dir": (im.width - logo.width - m, im.height - logo.height - m),
        "inf-esq": (m, im.height - logo.height - m),
        "sup-dir": (im.width - logo.width - m, m),
        "sup-esq": (m, m),
        "centro": ((im.width - logo.width) // 2, (im.height - logo.height) // 2),
    }[a.posicao]
    out = im.copy()
    out.alpha_composite(logo, pos)
    return out


def fundo(im, a):
    try:
        from rembg import remove
    except ImportError:
        sys.exit("Instale: pip install 'rembg[cpu]'  (ou use o conector Adobe: image_remove_background)")
    buf = io.BytesIO()
    im.save(buf, "PNG")
    recorte = Image.open(io.BytesIO(remove(buf.getvalue()))).convert("RGBA")
    if not a.cor:
        return recorte
    base = Image.new("RGBA", recorte.size, cor(a.cor) + (255,))
    if a.sombra:
        alfa = recorte.split()[-1]
        sombra = Image.new("RGBA", recorte.size, (0, 0, 0, 0))
        sombra.putalpha(alfa.point(lambda v: int(v * 0.35)))
        sombra = sombra.filter(ImageFilter.GaussianBlur(max(4, recorte.width // 80)))
        base.alpha_composite(sombra, (recorte.width // 100, recorte.height // 60))
    base.alpha_composite(recorte)
    return base


def comprimir(im, a, destino):
    if max(im.size) > a.max_lado:
        im = ImageOps.contain(im, (a.max_lado, a.max_lado), Image.LANCZOS)
    destino = os.path.splitext(destino)[0] + "." + a.formato
    if a.formato == "png":
        return salvar(im, destino)
    for q in range(90, 35, -5):
        buf = io.BytesIO()
        tmp = im if a.formato == "webp" else im.convert("RGB")
        tmp.save(buf, "WEBP" if a.formato == "webp" else "JPEG", quality=q, optimize=True)
        if buf.tell() <= a.max_kb * 1024:
            break
    salvar(im, destino, qualidade=q)


def moldura(im, a):
    lado = max(im.size)
    m = int(lado * a.margem)
    e = max(2, int(lado * a.espessura))
    W, H = im.width + 2 * m, im.height + 2 * m
    base = Image.new("RGBA", (W, H), cor(a.fundo) + (255,))
    base.alpha_composite(im, (m, m))
    borda = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    from PIL import ImageDraw
    d = ImageDraw.Draw(borda)
    c = cor(a.cor) + (255,)
    off = m // 2
    d.rectangle([off, off, W - off, H - off], outline=c, width=e)
    d.rectangle([off + e * 2, off + e * 2, W - off - e * 2, H - off - e * 2], outline=c, width=max(1, e // 3))
    base.alpha_composite(borda)
    return base


def info(p):
    im = Image.open(p)
    print(f"{p}: {im.width}x{im.height} {im.mode} {im.format} {os.path.getsize(p) // 1024} KB")


def arquivos(entrada, saida):
    if os.path.isdir(entrada):
        os.makedirs(saida, exist_ok=True)
        for n in sorted(os.listdir(entrada)):
            if os.path.splitext(n)[1].lower() in EXTS:
                yield os.path.join(entrada, n), os.path.join(saida, n)
    else:
        yield entrada, saida


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)

    s = sp.add_parser("tamanho"); s.add_argument("entrada"); s.add_argument("saida")
    s.add_argument("--preset", choices=PRESETS, required=True)
    s.add_argument("--modo", choices=["cobrir", "caber"], default="cobrir"); s.add_argument("--fundo")

    s = sp.add_parser("ajustar"); s.add_argument("entrada"); s.add_argument("saida")
    s.add_argument("--auto", action="store_true")
    for n in ("brilho", "contraste", "saturacao", "nitidez"):
        s.add_argument(f"--{n}", type=float, default=1.0)
    s.add_argument("--temperatura", type=int, default=0, help="+ quente, - frio (ex.: 12 ou -10)")

    s = sp.add_parser("marca"); s.add_argument("entrada"); s.add_argument("saida")
    s.add_argument("--logo", required=True)
    s.add_argument("--posicao", default="inf-dir", choices=["inf-dir", "inf-esq", "sup-dir", "sup-esq", "centro"])
    s.add_argument("--largura", type=float, default=0.22); s.add_argument("--opacidade", type=float, default=0.9)

    s = sp.add_parser("fundo"); s.add_argument("entrada"); s.add_argument("saida")
    s.add_argument("--cor"); s.add_argument("--sombra", action="store_true")

    s = sp.add_parser("comprimir"); s.add_argument("entrada"); s.add_argument("saida")
    s.add_argument("--formato", default="webp", choices=["webp", "jpg", "png"])
    s.add_argument("--max-kb", type=int, default=300); s.add_argument("--max-lado", type=int, default=2048)

    s = sp.add_parser("moldura"); s.add_argument("entrada"); s.add_argument("saida")
    s.add_argument("--cor", default="#C9A24A"); s.add_argument("--espessura", type=float, default=0.012)
    s.add_argument("--fundo", default="#0B0B0B"); s.add_argument("--margem", type=float, default=0.06)

    s = sp.add_parser("info"); s.add_argument("entrada")

    a = p.parse_args()
    if a.cmd == "info":
        for f, _ in arquivos(a.entrada, a.entrada):
            info(f)
        return
    for ent, sai in arquivos(a.entrada, a.saida):
        im = abrir(ent)
        if a.cmd == "comprimir":
            comprimir(im, a, sai)
            continue
        if a.cmd == "fundo" and not a.cor:
            sai = os.path.splitext(sai)[0] + ".png"  # transparência exige PNG
        out = {"tamanho": tamanho, "ajustar": ajustar, "marca": marca, "fundo": fundo, "moldura": moldura}[a.cmd](im, a)
        salvar(out, sai)


if __name__ == "__main__":
    main()
