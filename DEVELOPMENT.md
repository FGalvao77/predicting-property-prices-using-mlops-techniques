# Development Guide

Este documento descreve como desenvolver, testar e estender o projeto.

## 1. Visão rápida
- Código principal: `src/`
- Scripts principais:
  - `src/train.py` — treina o modelo e gera `top_features.json` e artefatos MLflow
  - `src/serve.py` — servidor FastAPI para inferência
  - `src/app.py` — cliente Streamlit (UI)
- Configuração compartilhada: `top_features.json`

## 2. Preparar ambiente de desenvolvimento
1. Crie e ative o venv (Windows):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1   # PowerShell
# ou
.venv\Scripts\activate        # cmd
```

2. Instale dependências (pip/poetry conforme preferir):

```powershell
# pip
pip install -r requirements.txt
# ou, se usar poetry e já inicializou o pyproject
poetry install
```

Se não existir `requirements.txt`, gere com:

```powershell
pip freeze > requirements.txt
```

## 3. Estrutura de código
- `src/data_prep.py` — carregamento, limpeza, seleção de features e scaling
- `src/train.py` — pipeline de treinamento e seleção de features
- `src/serve.py` — FastAPI app com endpoints `/health` e `/predict`
- `src/app.py` — Streamlit UI que consome `top_features.json` e chama `/predict`
- `top_features.json` — contrato de features (ordem + nomes amigáveis)

## 4. Executar localmente (fluxo de desenvolvimento)
1. Treinar modelo (gera `top_features.json` e artifacts MLflow):

```powershell
.venv\Scripts\activate
python src/train.py
```

2. Iniciar servidor FastAPI (modo desenvolvimento):

```powershell
.venv\Scripts\activate
uvicorn src.serve:app --host 0.0.0.0 --port 8000 --reload
```

3. Iniciar front-end Streamlit (modo headless quando necessário):

```powershell
$env:STREAMLIT_SERVER_HEADLESS='true'
.venv\Scripts\activate
python -m streamlit run src/app.py
```

4. Testar health:

```powershell
curl http://localhost:8000/health
```

5. Testar predição (exemplo curl):

```powershell
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"features":[8,2500,1500,500,600,1100,7500,400,2006,2]}'
```

## 5. Testes e linting
- Recomendado: `pytest`, `black`, `ruff` ou `flake8`.

Instalação (exemplo):

```powershell
pip install pytest black ruff
```

Rodar testes:

```powershell
pytest -q
```

Formatar código:

```powershell
black src/ tests/
ruff check src/ --fix
```

Adicionar testes básicos:
- `tests/test_data_prep.py` — validar shapes, tipos e ordenação de features
- `tests/test_serve.py` — usar `TestClient` do FastAPI para /health e /predict

Exemplo mínimo de teste de API (pytest):

```python
from fastapi.testclient import TestClient
from src.serve import app

client = TestClient(app)

def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    j = r.json()
    assert 'top_features' in j

def test_predict_shape():
    r = client.post('/predict', json={"features":[8,2500,1500,500,600,1100,7500,400,2006,2]})
    assert r.status_code == 200
    assert 'prediction' in r.json()
```

## 6. Como estender o pipeline (adicionar uma nova feature)
1. Atualize `src/data_prep.py` para garantir que a nova coluna seja carregada e processada (nome técnico consistente).
2. Atualize quaisquer mapeamentos de unidades em `FEATURES.md` e `top_features.json` (se aplicável).
3. Treine novamente:

```powershell
python src/train.py
```

Isso:
- treinará modelo inicial com todas as features
- extrairá importâncias
- gravará `top_features.json` com as 10 mais importantes
- retreinará modelo final e salvará artefatos

4. Atualize `src/app.py` caso queira inputs personalizados para a nova feature (ex.: slider, number_input).
5. Atualize documentação (`FEATURES.md`, `API_DOCUMENTATION.md`, `README.md`).

## 7. MLflow (experimentos)
- `train.py` registra métricas/params em `mlflow.db` (SQLite) e artifacts em `mlruns/`.
- Para visualizar UI do MLflow:

```powershell
mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --port 5000
# Acesse http://localhost:5000
```

## 8. Debugging rápido
- `Model not loaded` em `/health`: verifique existência de `top_features.json`, `mlflow.db` e `mlruns/.../artifacts/model.pkl`.
- Ordenação de features incorreta: compare `top_features.json` com a ordem usada pelo cliente.
- Erros de tipo ao chamar `/predict`: valide o JSON e tipos numéricos.
- Logs: rode `python src/serve.py` para ver prints/stack traces.

## 9. Boas práticas de commits e branches
- Branch: `feature/<short-descr>`, `fix/<short-descr>`, `chore/<short-descr>`
- Commit messages: imperativo e curto (ex.: `Add API docs for /predict`)
- Abra PRs pequenas, com screenshots/logs quando necessário.
- Execute `pytest` e `ruff`/`black` antes de abrir PR.

## 10. Pull request checklist
- [ ] Código formatado (`black`)
- [ ] Linter `ruff` sem erros críticos
- [ ] Testes relevantes adicionados/atualizados
- [ ] `top_features.json` atualizado quando necessário
- [ ] Documentação atualizada (`README.md`, `FEATURES.md`, `API_DOCUMENTATION.md`)

## 11. Docker (opcional)
- Dockerfile minimal:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "src.serve:app", "--host", "0.0.0.0", "--port", "8000"]
```

Construir e rodar:

```powershell
docker build -t mlops-boston .
docker run -p 8000:8000 mlops-boston
```

## 12. Próximos passos para desenvolvedores
- Adicionar testes unitários cobrindo `data_prep` e `serve`.
- Implementar CI (GitHub Actions) que rode `pytest`, `black --check` e `ruff`.
- Adicionar `Makefile` ou `npx` scripts para comandos repetitivos.

---

Se quiser, gero agora `CONTRIBUTING.md` com templates de PR e issues e um modelo de `CODE_OF_CONDUCT.md`.