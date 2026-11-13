#!/usr/bin/env python3
"""Gera imagem por IA usando uma API compatível com OpenAI Images.

Uso:
  IMAGE_API_KEY=... python3 gerar_imagem.py "prompt" saida.png [--size 1024x1024] [--n 1]

Variáveis de ambiente:
  IMAGE_API_KEY   chave do provedor (obrigatória; nunca commitar)
  IMAGE_API_BASE  URL base (padrão: https://api.openai.com/v1)
  IMAGE_MODEL     modelo (padrão: gpt-image-1; confira o nome atual na documentação)
"""
import argparse
import base64
import json
import os
import sys
import urllib.request


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("prompt")
    p.add_argument("saida")
    p.add_argument("--size", default="1024x1024")
    p.add_argument("--n", type=int, default=1)
    a = p.parse_args()

    key = os.environ.get("IMAGE_API_KEY")
    if not key:
        print("Defina IMAGE_API_KEY com a chave do provedor de imagens.", file=sys.stderr)
        return 1
    base = os.environ.get("IMAGE_API_BASE", "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("IMAGE_MODEL", "gpt-image-1")

    body = json.dumps({"model": model, "prompt": a.prompt, "size": a.size, "n": a.n}).encode()
    req = urllib.request.Request(
        f"{base}/images/generations",
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        print(f"Erro {e.code}: {e.read().decode(errors='replace')}", file=sys.stderr)
        return 1

    raiz, ext = os.path.splitext(a.saida)
    ext = ext or ".png"
    for i, item in enumerate(data.get("data", [])):
        destino = a.saida if a.n == 1 else f"{raiz}-{i + 1}{ext}"
        if item.get("b64_json"):
            with open(destino, "wb") as f:
                f.write(base64.b64decode(item["b64_json"]))
        elif item.get("url"):
            urllib.request.urlretrieve(item["url"], destino)
        else:
            continue
        print(destino)
    return 0


if __name__ == "__main__":
    sys.exit(main())
