# Request Examples

Exemplos de como chamar a API `/predict` e `/health`.

## Curl (bash)

```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [8,2500,1500,500,600,1100,7500,400,2006,2] }'
```

## PowerShell

```powershell
Invoke-RestMethod -Method Get -Uri http://localhost:8000/health

$body = @{ features = @(8,2500,1500,500,600,1100,7500,400,2006,2) } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://localhost:8000/predict -Body $body -ContentType 'application/json'
```

## Python (requests)

```python
import requests
url = 'http://localhost:8000/predict'
payload = { 'features': [8,2500,1500,500,600,1100,7500,400,2006,2] }
resp = requests.post(url, json=payload)
print(resp.status_code, resp.json())
```

## JavaScript (fetch)

```javascript
fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ features: [8,2500,1500,500,600,1100,7500,400,2006,2] })
}).then(r => r.json()).then(console.log);
```
