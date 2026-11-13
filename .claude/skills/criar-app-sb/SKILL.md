---
name: criar-app-sb
description: Use ao criar, melhorar ou corrigir apps do Samuel (SB Desenvolvedor de apps): HTML/JS mobile-first, Supabase, PWA/APK, visual de vendas.
---

# Criar apps no padrão SB Desenvolvedor de Apps

Responda em português do Brasil. O Samuel trabalha pelo celular Android: passos curtos, dizendo exatamente onde tocar.

## 1. Entender antes de construir
- Confirme em 1 a 3 perguntas só o que muda o resultado: nome e marca, quem usa, funções principais, login e pagamento.
- Se o app já existe, leia o código primeiro e mantenha estilo, paleta e logos.

## 1.1 Demo primeiro, depois o app
- Antes de construir, crie uma **demo clicável** (HTML único, dados fictícios, sem backend) mostrando as telas
  principais e o fluxo de uso. Publique como página (Artifact) e mande o link para o Samuel abrir no celular.
- Junto da demo, ofereça **3 a 5 ideias** de funções que aumentem vendas ou poupem tempo, em lista curta.
- Pergunte: "Aprova assim ou quer ajustar algo?". Só depois da aprovação ligue Supabase, login e pagamentos.

## 2. Stack padrão
- HTML + CSS + JS puro, mobile-first; arquivo HTML único quando possível.
- Supabase (auth, Postgres, storage) com RLS em toda tabela; só a chave pública no front. Firebase só se precisar de tempo real.
- Funcionar como PWA e poder virar APK/AAB (skill `play-store-android`).
- Pagamentos por API: skill `pagamentos-pix-api`. Banco: skills `supabase` e `supabase-postgres-best-practices`.

## 3. Estrutura de todo app de gestão
- Login, cadastro, recuperação de senha e **exclusão de conta**.
- Painel admin para liberar clientes, com validade exata (dd/mm/aaaa, America/Sao_Paulo).
- Aba "Suporte e Planos" ligada ao WhatsApp (wa.me com mensagem pronta).
- CRUD completo em cada lista; compartilhar/exportar em PDF ou imagem quando fizer sentido.
- Sem teste grátis, a menos que o Samuel peça.

## 4. Checklist antes de entregar
- 360–412 px: nada cortado, sem rolagem lateral, botões ≥ 44 px.
- Visual limpo, profissional, de vendas (skill `frontend-design`), logos mantidas.
- Ortografia revisada em todos os textos.
- Todo botão mostra carregando, sucesso ou erro; nada trava.
- Testar o fluxo principal de ponta a ponta (skill `webapp-testing`) e tirar print em tamanho de celular.
- Demos e vídeos com dados fictícios e sem dados bancários reais.

## 5. Entrega
- Commit curto em português; listar o que mudou, como testar no celular e o próximo passo.
