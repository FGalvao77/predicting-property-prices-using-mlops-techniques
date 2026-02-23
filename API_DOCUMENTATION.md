# API Documentation

Este documento descreve a API exposta pelo servidor FastAPI para servir o modelo de precificação de imóveis.

Base URL (local):

```text
http://localhost:8000
```

## Como iniciar o servidor

No venv do projeto execute:

```powershell
$env:POETRY_ACTIVE='' # se necessário
.venv\Scripts\activate
python src/serve.py
```

ou (uvicorn explícito):

```powershell
.venv\Scripts\activate
uvicorn src.serve:app --host 0.0.0.0 --port 8000 --reload
```

## Endpoints

### GET /health

- Descrição: Verifica se o servidor e o modelo estão carregados e retorna a lista de features esperadas.
- Método: `GET`
- URL: `/health`

Resposta de sucesso (200 OK):

```json
{
  "status": "healthy",
  "model_loaded": true,
  "top_features": [
    "OverallQual",
    "GrLivArea",
    "TotalBsmtSF",
    "2ndFlrSF",
    "BsmtFinSF1",
    "1stFlrSF",
    "LotArea",
    "GarageArea",
    "YearBuilt",
    "GarageCars"
  ],
  "n_features": 10
}
```

Erros possíveis:
- 500 Internal Server Error: falha ao carregar o modelo ou arquivo de configuração.

### POST /predict

- Descrição: Recebe um array com exatamente `n_features` (normalmente 10) valores numéricos na ordem definida em `top_features` e retorna a predição do preço.
- Método: `POST`
- URL: `/predict`
- Headers: `Content-Type: application/json`

Request body schema:

```json
{
  "features": [number, number, ..., number]
}
```

Regras de validação importantes:
- O campo `features` é obrigatório.
- Deve ser um array de números com comprimento igual a `n_features` (ver `/health`).
- A ordem dos valores deve corresponder exatamente à ordem listada em `top_features`.

Exemplo de requisição (curl):

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [8, 2500, 1500, 500, 600, 1100, 7500, 400, 2006, 2]
  }'
```

Exemplo em Python (requests):

```python
import requests

url = "http://localhost:8000/predict"
payload = {
    "features": [8, 2500, 1500, 500, 600, 1100, 7500, 400, 2006, 2]
}
resp = requests.post(url, json=payload, timeout=5)
print(resp.status_code, resp.json())
```

Exemplo em JavaScript (fetch):

```javascript
fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ features: [8,2500,1500,500,600,1100,7500,400,2006,2] })
})
.then(r=>r.json()).then(console.log).catch(console.error)
```

Resposta de sucesso (200 OK):

```json
{
  "prediction": 564320.51
}
```

Erros e códigos de resposta:

- 400 Bad Request
  - Quando o JSON está malformado, falta o campo `features`, ou `features` não é um array de números.
  - Quando o comprimento do array não corresponde a `n_features`.
  - Exemplo: `{ "error": "Expected 10 features, got 9" }`.

- 422 Unprocessable Entity
  - Validação de esquema JSON (FastAPI/Pydantic) falhou por tipo incorreto.

- 500 Internal Server Error
  - Modelo não carregado ou erro interno durante preprocessamento/predição.

## Ordem e nomes das features (contrato)

A API espera os valores na mesma ordem definida em `top_features.json`. Antes de enviar requisições, consulte `/health` para confirmar o `top_features` ativo.

Exemplo (ordem canônica):
1. OverallQual
2. GrLivArea
3. TotalBsmtSF
4. 2ndFlrSF
5. BsmtFinSF1
6. 1stFlrSF
7. LotArea
8. GarageArea
9. YearBuilt
10. GarageCars

(Se o seu cliente/Front-end usar nomes amigáveis, é responsabilidade do cliente mapear para esta ordem antes de enviar.)

## Preprocessamento esperado

O servidor aplica o mesmo `StandardScaler` usado no treinamento. Envie valores brutos (unscaled). O servidor realiza a normalização antes de alimentar o modelo.

## Segurança e limites

- Não envie dados sensíveis; o serviço não persiste entradas por design.
- Não há autenticação por padrão; em produção, adicione OAuth2/API keys/Ingress rules.
- Recomenda-se configurar rate-limiting e CORS conforme seus requisitos.

## Testes rápidos

1. Verifique `/health`:

```bash
curl http://localhost:8000/health
```

2. Envie uma predição de exemplo (curl acima).

3. Se receber `Expected 10 features`, ajuste o array para o tamanho correto.

## Troubleshooting

- Problema: `Model not loaded` ou `model_loaded: false` em `/health`.
  - Verifique se `top_features.json` está na raiz do projeto e se `mlruns/<exp_id>/<run_id>/artifacts/model.pkl` existe.
  - Logs: rode `python src/serve.py` em terminal para ver mensagens de erro.

- Problema: `422` ou `400` ao postar JSON.
  - Confirme `Content-Type: application/json` e o formato do corpo.
  - Valide que todos os elementos em `features` são numéricos.

- Problema: Predições absurdas
  - Confirme que a ordem das features está correta e que valores estão em unidades esperadas (m2, anos, contagens).

## Versionamento da API

Esta documentação corresponde à versão atual do servidor local. Para mudanças de contrato (ordem/contagem de features), incremente a versão da API e mantenha endpoints compatíveis quando possível.

## Integração rápida com Streamlit (cliente)

No `src/app.py` o cliente lê `top_features.json` e monta os inputs nessa mesma ordem; a rotina envia o array ordenado para `/predict` e exibe o resultado formatado.

---

**Próximo passo sugerido:** gerar `FEATURES.md` com descrições, ranges e importância de cada uma das 10 features.  
