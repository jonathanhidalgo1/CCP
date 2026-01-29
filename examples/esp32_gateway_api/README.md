# ESP32 -> Python Gateway API (FastAPI)

Este exemplo mostra um **gateway** em Python que recebe dados do ESP32 via HTTP e, internamente, chama um servidor CCP usando o `ccp-sdk`.

## Como executar

1) Instale dependências:

```bash
python -m pip install -r requirements.txt
```

2) Configure o servidor CCP alvo (pode ser o exemplo `examples/ccp_api` rodando em `:8000`):

```bash
export CCP_BASE_URL=http://127.0.0.1:8000
```

3) Rode o gateway:

```bash
uvicorn main:app --reload --port 9000
```

## Endpoints (para o ESP32)

- `GET /health`
- `POST /esp32/hello`
- `POST /esp32/session/start`
- `POST /esp32/turn/text`
- `POST /esp32/turn/audio/{device_id}` (body = bytes de áudio)
- `POST /esp32/session/end`

## Observações
- Sessões são armazenadas em memória (dict). Em produção, use Redis/DB.
- Este exemplo assume que o ESP32 envia `device_token` e o gateway usa esse token para autenticar no servidor CCP.
