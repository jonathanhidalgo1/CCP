# CCP API Example (FastAPI)

Exemplo mínimo de API HTTP que implementa o fluxo básico do CCP.

## Como executar
1) Instale as dependências com o `requirements.txt`.
2) Inicie o servidor com `uvicorn main:app --reload --port 8000`.

## Endpoints
- `GET /health`
- `POST /ccp/hello`
- `POST /ccp/session/start`
- `POST /ccp/turn`
- `POST /ccp/session/end`

## Observações
- Este exemplo faz apenas validação de payload e responde com mensagens CCP válidas.
- Para produção, conecte autenticação real, armazenamento de sessões e pipeline de áudio.
