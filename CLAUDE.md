# CLAUDE.md — Padrão SB Desenvolvedor de Apps

Responda sempre em **português do Brasil**. O dono é o Samuel, que trabalha **pelo celular Android**.
Explique em passos curtos e diretos, sem jargão. Quando ele precisar fazer algo, diga exatamente onde tocar.

## O que é este projeto
**Rifa Pro**: app para criar e gerenciar rifas. Um arquivo só (`index.html`) com o painel do dono
(login, campanhas, fotos do prêmio, reservas, marcar como pago) e a página pública da rifa
(`?r=slug`), onde o cliente escolhe números, reserva e paga por Pix/WhatsApp.
- Site: https://sbdesignerdeepoca-crypto.github.io/rifa-pro/ (GitHub Pages, ramo `main`, pasta raiz).
- `PUBLIC_SITE_URL` no código precisa ser o endereço do site, senão o link público não funciona.
- Supabase: tabelas `raffles`, `raffle_tickets`, `raffle_reservations`, bucket `raffle-prizes`
  e a Edge Function `reserve-raffle-tickets`.

## Stack padrão
- **Front:** HTML + CSS + JavaScript puro. O padrão é um **arquivo HTML único**, que abre direto no celular
  e é fácil de hospedar e de empacotar. Não usar frameworks pesados sem pedido.
- **Backend:** **Supabase** (auth, banco Postgres, storage). Firebase só se precisar de tempo real.
  - Toda tabela com **RLS ligado** e políticas por usuário.
  - Nunca colocar a chave `service_role` no front. No HTML vai só a chave pública (anon/publishable).
- **Android:** o app precisa funcionar como PWA e poder virar APK/AAB (WebView/Capacitor).
- **Hospedagem:** estática (GitHub Pages, Cloudflare Pages ou similar).

## Padrão de qualidade ("app top")
1. **Mobile-first**: testar em largura de 360–412 px. Botões com pelo menos 44 px, nada cortado e sem rolagem lateral.
2. **Visual profissional e limpo**, voltado a vendas e nada poluído. Paleta e logo de cada projeto preservadas.
   **Nunca remover marcas ou logos** existentes sem pedido.
3. **Ortografia perfeita** em todo texto da interface, sem erros de digitação.
4. **Nada trava**: todo botão mostra carregando, sucesso ou erro. Mensagens de erro em português claro.
5. **Dados seguros**: validar campos, tratar internet ruim e nunca perder o que o usuário digitou.
6. **WhatsApp** com link `https://wa.me/55DDDNUMERO` e mensagem pronta e editável.
7. **Datas e validade** de assinatura sempre exatas, no fuso America/Sao_Paulo e no formato dd/mm/aaaa.
8. **Sem teste grátis**: não exibir "teste de 7 dias" nem "Experimente grátis".
9. Para vídeos e demos, usar **dados fictícios** e esconder dados bancários reais.

## Como trabalhar
- **Demo antes de criar:** quando o Samuel pedir um app novo (ou uma tela/função grande), primeiro montar
  uma **demo visual clicável** (HTML com dados fictícios) e mandar o link para ele ver no celular.
  Só construir de verdade (Supabase, login, pagamentos) **depois que ele aprovar** ou pedir ajustes.
- **Trazer ideias:** junto da demo, sugerir de 3 a 5 ideias práticas que ajudem a vender mais ou poupar
  tempo (ex.: mensagem pronta no WhatsApp, ranking de clientes, relatório da live). Ele escolhe o que entra.
- Agir como programador profissional: código organizado, seguro e testado no tamanho de celular.
- Antes de mudar, ler o código existente e manter o estilo dele.
- Mudanças pequenas e testáveis. Ao terminar, listar **o que mudou** e **como testar no celular**.
- Commits em português, curtos: `corrige login travado`, `adiciona envio de nota em PDF`.
- Não apagar funcionalidades existentes sem confirmar com o Samuel.
- Se faltar informação que muda o resultado (ex.: chave do Supabase, número de WhatsApp), perguntar.

## Skills deste repositório (`.claude/skills/`)
- `criar-app-sb`: seu padrão para criar e melhorar apps.
- `play-store-android`: Capacitor, AAB, versões e checklist da Play Console.
- `pagamentos-pix-api`: Pix/cartão por API com Supabase Edge Functions e webhook.
- `supabase` e `supabase-postgres-best-practices`: oficiais do Supabase (auth, RLS, migrações, segurança).
- `frontend-design`: visual caprichado e fora do padrão genérico.
- `webapp-testing`: testar o app no navegador (Playwright) e tirar prints.
- `skill-creator`: criar novas skills quando surgir um processo repetido.
- `logos-e-artes`: logos, ícones, banners e posts (SVG para texto perfeito + IA de imagem para fotos).
- `canvas-design`: artes e pôsteres em PNG/PDF, com fontes profissionais (OFL) incluídas.
- `theme-factory`: paletas e combinações de fontes prontas ou sob medida.
- `edicao-de-imagens`: remover fundo, recortar para post/story/Play, luz e cor, logo/marca d'água, moldura, comprimir e lote.
- `fotos-de-produto`: padrão de vitrine para peças, móveis e prêmios, cards de preço e catálogo.

## Segredos
Chaves secretas (token de pagamento, `service_role`, keystore `.jks`) **nunca** vão para o repositório nem para o HTML.
Ficam em Supabase secrets ou em GitHub Actions Secrets. O `.gitignore` já bloqueia os arquivos comuns.
