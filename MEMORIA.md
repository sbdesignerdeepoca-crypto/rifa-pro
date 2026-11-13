# MEMORIA.md — o que já aprendemos com o Samuel

Notas das conversas anteriores. Leia antes de começar e **atualize ao final** de cada conversa
com o que for importante (decisões, problemas resolvidos, pendências). Nunca salvar senhas,
chaves secretas, Pix, telefone ou e-mail pessoal aqui (o repositório rifa-pro é público).

## Jeito de trabalhar com o Samuel
- Trabalha só pelo **celular Android** (Chrome). **Não quer digitar código**: eu faço tudo que der;
  para ele, só passos de **tocar na tela**, um por linha, dizendo onde fica cada botão.
- Quando uma tela do GitHub/Supabase não mostrar opções no celular: pedir para ligar
  **Chrome → 3 pontinhos → "Versão para computador"** e mandar **print**.
- Gosta de ver antes: **demo/prévia primeiro** (imagem ou página) e opções para escolher (A, B, C).
- Sempre trazer **ideias** para vender mais junto com a entrega.

## Contas e acessos
- GitHub: `sbdesignerdeepoca-crypto`.
  - `gestao-de-lives` (privado): padrão SB, skills.
  - `rifa-pro` (público): app de rifas, publicado no GitHub Pages (ramo `main`, pasta raiz).
- Configurações do GitHub (ligar Pages, permissões, apps) **só o Samuel consegue mudar**. Eu não tenho acesso.
- Supabase do Rifa Pro: projeto `hwussryznzedbaebadpp`.
  - O conector do Supabase aqui está ligado a **outra conta** (projetos "oraculo-de-ifa" e outro).
    Para eu mexer no banco do Rifa Pro, ele precisa reconectar o Supabase com a conta certa em
    claude.ai/customize/connectors e abrir uma conversa nova.
  - O container da nuvem **não acessa** `*.supabase.co` nem sites `github.io`: não dá para testar
    o site daqui; pedir print para ele.

## Lições (problemas que já resolvemos)
- **Link público quebrado** quando o app é aberto como arquivo (Drive/`content://`): o link sai com
  endereço do celular. Solução: hospedar no GitHub Pages e fixar `PUBLIC_SITE_URL` no código.
- **raw.githack.com** mostra uma tela de aviso antes do app: serve só como teste provisório.
- Rifa nova nascia como **rascunho** e o link dava "Rifa não encontrada": agora nasce publicada
  e o painel mostra o botão "Publicar agora".
- **Data do sorteio** adiantava 3 h a cada edição (UTC × horário local): corrigido; exibir sempre
  no fuso America/Sao_Paulo.
- Esqueceu a senha: o app tem "Esqueci minha senha". Sem acesso ao banco, a saída rápida é o SQL
  no SQL Editor do Supabase (`update auth.users set encrypted_password = extensions.crypt(...)`).
- GitHub às vezes responde 503: repetir o push com espera.

## Pendências (atualizar sempre)
- [ ] Samuel escolher a **logo do Rifa Pro** (A bilhete dourado, B monograma R, C bola de sorteio)
      e eu aplicar no topo, ícone da tela inicial, aba e prévia do WhatsApp.
- [ ] Juntar o PR #1 do gestao-de-lives (regra "demo antes + ideias").
- [ ] Conferir a data/hora do sorteio da rifa "Contribuição no meu novo projeto" (aparecia 04:03).
- [ ] No Supabase do Rifa Pro: Authentication → URL Configuration → colocar o endereço do site
      (para o link de "Esqueci minha senha" voltar para o app).
- [ ] Ideias oferecidas para o Rifa Pro: barra de progresso, ranking de compradores, botão de
      compartilhar no WhatsApp, contagem regressiva, pacotes promocionais.
