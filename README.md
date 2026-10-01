# Alerta de meme coin nos posts do Trump

Fluxo: serviço de origem detecta o post → `POST /webhook` → Claude classifica → notificação no celular via ntfy.

## Rodar

```
pip install -r requirements.txt
cp .env.example .env   # preencha e exporte as variaveis
uvicorn bot:app --host 0.0.0.0 --port 8000
```

Instale o app **ntfy** no celular e assine o mesmo tópico de `NTFY_TOPIC`.

## Testar

```
curl -X POST localhost:8000/webhook -H "X-Webhook-Secret: SEU_SEGREDO" \
  -H "Content-Type: application/json" \
  -d '{"id":"1","text":"Everyone should check out $TRUMP, the best memecoin!"}'
```

O endpoint aceita os campos `text`, `full_text`, `tweet`, `content` ou `message`, e `id`, `url`/`link` quando existirem.

## Origem dos posts

Qualquer serviço que faça POST com o texto serve (Zapier, IFTTT, Make, Apify com webhook, X API).
O Trump posta principalmente no Truth Social; no X o perfil é `@realDonaldTrump`.
