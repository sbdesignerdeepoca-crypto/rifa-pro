---
name: pagamentos-pix-api
description: Use ao integrar recebimento por Pix/cartão via API (Mercado Pago, Asaas, Efí, PagBank etc.) em apps com Supabase: cobrança, QR Code, webhook de confirmação e baixa automática.
---

# Receber pagamentos direto no app (Pix por API + Supabase)

## Regras de ouro
1. **Chaves secretas só no servidor**: access token, client secret e certificados ficam em **Supabase Edge Functions** (secrets). Nunca no HTML, no APK ou no repositório.
2. **Quem confirma o pagamento é o webhook**, nunca o celular do cliente. Tela de "paguei" não libera nada sozinha.
3. **Valor calculado no servidor** a partir do banco (pedido, peça, número da rifa), nunca o valor enviado pelo front.
4. **Idempotência**: o mesmo webhook pode chegar mais de uma vez. Use o `id` do pagamento do gateway como chave única.
5. Antes de usar a API de um gateway, **consulte a documentação oficial atual** dele (endpoints, campos, assinatura do webhook). Não invente campos.
6. Para app na Play Store, veja a seção de pagamentos da skill `play-store-android` (assinatura do próprio app ≠ venda de produto físico).

## Arquitetura padrão
```
App (HTML/JS) ──supabase-js──> Edge Function `criar-cobranca`
                                   │ cria pedido "pendente" no banco
                                   │ chama a API do gateway (token secreto)
                                   └─> devolve QR Code / copia-e-cola + validade
Gateway ──POST──> Edge Function `webhook-pagamento`
                     │ valida a assinatura/segredo do webhook
                     │ consulta o pagamento na API do gateway (não confia só no corpo)
                     └─> atualiza pedido para "pago" (uma vez só)
App ──Realtime ou consulta──> mostra "Pagamento confirmado ✅"
```

## Tabela base (ajuste ao app)
```sql
create table pagamentos (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id),
  referencia text not null,            -- ex.: id da venda, da rifa, do pedido
  valor_centavos integer not null check (valor_centavos > 0),
  status text not null default 'pendente' check (status in ('pendente','pago','expirado','cancelado','estornado')),
  gateway text not null,
  gateway_payment_id text unique,      -- idempotência
  pix_copia_cola text,
  expira_em timestamptz,
  pago_em timestamptz,
  criado_em timestamptz not null default now()
);
alter table pagamentos enable row level security;
create policy "dono lê os seus" on pagamentos for select using (auth.uid() = user_id);
-- inserts/updates só pelas Edge Functions (service role), sem policy de escrita para o cliente
```

## Edge Functions
- `criar-cobranca`: autentica o usuário (JWT), busca o item no banco, calcula o valor, cria a cobrança no gateway com `external_reference` = id do pagamento e salva o QR/copia-e-cola.
- `webhook-pagamento`: deploy com verificação de JWT **desligada** (o gateway não manda JWT), mas **valida o segredo/assinatura do gateway**. Responde 200 rápido; status desconhecido → registra e ignora.
- Segredos: `supabase secrets set GATEWAY_TOKEN=... WEBHOOK_SECRET=...`.

## Experiência no app
- Mostrar QR Code, botão **"Copiar código Pix"**, valor em R$ (formato `R$ 1.234,56`) e contagem regressiva da validade.
- Atualizar sozinho quando pagar (Realtime na linha do pagamento ou consulta a cada 5 s, por até a validade).
- Pix expirado → botão "Gerar novo Pix". Erros em português claro.
- Comprovante: opção de compartilhar no WhatsApp e gerar PDF.

## Teste antes de produção
- Usar o **ambiente sandbox/teste** do gateway e credenciais de teste.
- Testar: pagamento aprovado, webhook repetido (não duplica), Pix expirado, valor adulterado no front (servidor ignora) e usuário vendo pagamento de outro (RLS bloqueia).
