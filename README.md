# Rifa Pro

Aplicativo de campanhas e reservas em HTML, CSS e JavaScript, com autenticação, banco e fotos no Supabase.

- Painel: https://sbdesignerdeepoca-crypto.github.io/rifa-pro/
- Campanha pública: `?r=slug-da-campanha`
- Prévia com dados fictícios: `previa.html`

## Versão definitiva

O `index.html` usa os dados reais do projeto Supabase existente. Inclui painel com totais de reservas pagas e pendentes, campanhas restritas ao proprietário, galeria do prêmio, seleção manual ou aleatória, busca e paginação, resumo antes da reserva, Pix por chave, WhatsApp e exportação CSV.

A confirmação do Pix continua **manual**, após conferência do recebimento pelo organizador. Não há provedor de pagamentos, QR Code de cobrança automática, aprovação automática ou expiração automática de reservas nesta versão. A reserva pública continua usando a Edge Function `reserve-raffle-tickets` e a função transacional já existentes no banco. Confirmar/cancelar continua usando o gatilho existente para sincronizar os números.

Campanhas novas começam internamente como rascunho. Os números são inseridos em uma única operação, a quantidade é conferida e só então o status solicitado é aplicado. Se a geração falhar, a edição fica aberta para retomar com **Salvar**, sem publicar uma grade incompleta. Um rascunho também pode ser reaberto para completar sua quantidade.

O manifesto e os ícones permitem adicionar o aplicativo à tela inicial. O service worker usa a rede primeiro e armazena somente o HTML estático; sessões e respostas do Supabase não são armazenadas por ele. É necessário internet para autenticar, consultar disponibilidade e gravar alterações.

## Publicação e acesso

GitHub Pages publica o ramo `main`, pasta raiz. O aplicativo deve ser aberto pelo endereço HTTPS; arquivos abertos via `content://` no Android não oferecem a mesma compatibilidade com autenticação, instalação e área de transferência.

Em Supabase → Authentication → URL Configuration, o endereço principal precisa estar autorizado para confirmação de cadastro e recuperação de senha. Somente a chave pública do projeto fica no HTML; políticas RLS continuam limitando a administração ao proprietário. Não colocar chaves administrativas, senhas ou tokens no repositório.

## Testes

Instale Playwright e Chromium e execute:

```sh
python -m pip install playwright
python -m playwright install chromium
python tests/test_app.py
```

Para usar um Chromium já instalado, defina `CHROMIUM_EXECUTABLE`. Os testes interceptam o SDK e usam apenas dados fictícios em memória: não criam contas, campanhas ou reservas reais. Cobrem 1.300 números, seleção, busca, paginação, reserva, falha de rede, pagamento/cancelamento, isolamento do proprietário no painel, CSV, fuso de Brasília, criação interrompida e retomada. Capturas ficam na pasta temporária `rifa-pro-tests` (ou em `TEST_ARTIFACT_DIR`).
