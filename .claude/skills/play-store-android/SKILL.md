---
name: play-store-android
description: Use ao empacotar um app HTML/JS como Android (Capacitor), gerar AAB/APK, subir nova versão, corrigir rejeição ou preparar a ficha na Google Play Console.
---

# Publicar e atualizar apps Android na Play Store

O Samuel trabalha pelo celular. Diga sempre exatamente onde tocar na Play Console.

## 1. Empacotamento (Capacitor)
- Projeto web em `www/` (ou `dist/`) com `index.html`. Config em `capacitor.config.json`:
  `appId` no formato `br.com.marca.app` (**nunca mudar depois de publicado**), `appName` e `webDir`.
- Comandos: `npm i @capacitor/core @capacitor/cli @capacitor/android` → `npx cap init` → `npx cap add android` → `npx cap sync android`.
- Ícone e splash: `@capacitor/assets` a partir de uma imagem de 1024×1024.
- Links `wa.me`, `tel:` e PDFs devem abrir fora da WebView (`@capacitor/browser` ou `window.open(url, '_system')`).
- Botão voltar do Android: tratar com `@capacitor/app` (`backButton`) para não fechar o app sem querer.

## 2. Gerar o AAB
- A cada envio, **subir `versionCode`** (inteiro, sempre maior) e `versionName` (ex.: 1.0.3) em `android/app/build.gradle`.
- Assinar com a **mesma chave de upload** de sempre. Se a chave for perdida, só o suporte do Google redefine. Guarde o `.jks` e as senhas fora do repositório (nunca commitar).
- Build: `cd android && ./gradlew bundleRelease` → `app/build/outputs/bundle/release/app-release.aab`.
- Sem PC: usar um workflow no GitHub Actions que gera o AAB com a chave guardada em *Secrets* e deixa o arquivo para baixar no celular.
- Conferir no `build.gradle` se o `targetSdkVersion` atende à exigência **atual** da Play (ela sobe todo ano; consulte a página "Target API level requirements" antes de publicar).

## 3. Trilhas de teste
- Teste interno (até 100 testadores, sem revisão demorada) → teste fechado → produção.
- Contas pessoais novas exigem **teste fechado com testadores ativos por um período mínimo** antes de liberar produção; confira o número e os dias atuais na Play Console (Painel → "Publicar app").

## 4. Checklist da ficha (evita rejeição)
- **Política de privacidade** em URL pública (pode ser uma página no GitHub Pages).
- **Segurança dos dados**: declarar tudo o que o app coleta (nome, telefone/WhatsApp, e-mail, dados de compra) e se há criptografia em trânsito (Supabase usa HTTPS: sim).
- **Exclusão de conta**: o app precisa permitir excluir a conta *e* ter um link web para pedir exclusão.
- Acesso para revisão: se tem login, fornecer **usuário e senha de teste** em "Acesso ao app".
- Classificação de conteúdo, público-alvo, anúncios (sim/não), categoria.
- Capturas de tela reais do app, ícone 512×512 e banner 1024×500 com ortografia revisada, logos mantidas e **sem "teste grátis"** se o app não oferece.

## 5. Pagamentos dentro do app (regra crítica)
- Vender **acesso ao próprio app** (assinatura, plano, desbloqueio de funções) dentro do app instalado pela Play exige, em regra, o **Google Play Billing**. Pix ou link externo para isso pode causar suspensão. Confira a política "Pagamentos" atual antes.
- Receber por **produtos físicos ou serviços fora do app** (peças da live, rifa de prêmio físico, serviço de salão) pode usar Pix ou gateway próprio. Veja a skill `pagamentos-pix-api`.
- Na dúvida, avise o Samuel do risco antes de implementar.

## 6. Ao terminar
Informe a versão gerada (versionName/versionCode), o que mudou, onde está o AAB e os passos na Play Console:
Testar e lançar → Teste interno → Criar nova versão → enviar o AAB → notas da versão → Revisar → Lançar.
