# 📖 Guia Completo de Configuração do Ambiente

Este documento fornece instruções passo a passo para configurar o ambiente de desenvolvimento do projeto MLOps Boston House Price Prediction.

## 📋 Pré-requisitos

### Sistema Operacional
- Windows 10/11
- Linux (Ubuntu 20.04+)
- macOS 10.14+

### Software Necessário
- Python 3.13+ ([Download](https://www.python.org/downloads/))
- Git ([Download](https://git-scm.com/downloads))
- Um editor de código (VS Code recomendado)

### Versão Python
```bash
python --version
# Python 3.13.12 (ou superior)
```

## 🔧 Passo 1: Preparar o Ambiente

### 1.1 Clonar o Repositório

```bash
# Usar HTTPS
git clone https://github.com/seu-usuario/mlops-boston-project.git
cd mlops-boston-project

# OU usar SSH (se configurado)
git clone git@github.com:seu-usuario/mlops-boston-project.git
cd mlops-boston-project
```

### 1.2 Criar Ambiente Virtual

**Windows:**
```bash
# Criar venv
python -m venv .venv

# Ativar venv
.venv\Scripts\activate

# Verificar se ativado (deve mostrar (.venv) no prompt)
# C:\...\mlops-boston-project> (.venv) C:\...\mlops-boston-project>
```

**Linux/macOS:**
```bash
# Criar venv
python3 -m venv .venv

# Ativar venv
source .venv/bin/activate

# Verificar se ativado (deve mostrar (.venv) no prompt)
# (venv) user@machine:~/mlops-boston-project$
```

### 1.3 Atualizar pip, setuptools e wheel

```bash
# Windows
python -m pip install --upgrade pip setuptools wheel

# Linux/macOS
python3 -m pip install --upgrade pip setuptools wheel
```

## 📦 Passo 2: Instalar Dependências

### Opção A: Usar Poetry (Recomendado)

**Instalar Poetry:**
```bash
pip install poetry
```

**Instalar dependências do projeto:**
```bash
poetry install
```

**Verificar instalação:**
```bash
poetry --version
```

### Opção B: Usar pip com requirements.txt

```bash
# Instalar todas as dependências
pip install -r requirements.txt
```

:bulb: **Sugestão de boa prática na instalação de bibliotecas**

Não utilize o `cache` ao instalar as bibliotecas. Mas afinal, o por quê?

Ao instalar bibliotecas com o `--no-cache-dir`, isso reduz o risco de vulnerabilidades e bugs de segurança e garante que as dependências seja mais atualizadas e seguras.

```bash
pip install --no-cache-dir -r requirements.txt
```

```bash
# Verificar instalação
pip list
```

## 📚 Dependências Principais

| Pacote | Versão | Propósito |
|--------|--------|----------|
| pandas | 2.3.3 | Processamento de dados |
| numpy | 2.4.2 | Computação numérica |
| scikit-learn | - | Machine Learning |
| mlflow | - | Model tracking e registry |
| fastapi | - | API REST |
| uvicorn | - | ASGI server |
| streamlit | 1.54.0 | Interface web |
| prometheus-client | - | Métricas (opcional) |
| requests | - | Cliente HTTP |
| pytest | - | Testes |

## 🏗️ Passo 3: Estrutura do Projeto

Após clonar, sua estrutura deve ser:

```
mlops-boston-project/
│
├── src/
│   ├── __init__.py
│   ├── data_prep.py         # Preparação de dados
│   ├── train.py             # Treinamento do modelo
│   ├── serve.py             # API FastAPI
│   └── app.py               # Interface Streamlit
│
├── mlruns/                  # Artefatos MLflow (gerado após treinar)
├── mlflow.db                # Banco de dados SQLite MLflow (gerado após treinar)
│
├── .venv/                   # Ambiente virtual Python
│
├── .gitignore               # Arquivos ignorados pelo Git
├── pyproject.toml           # Definição do projeto Poetry
├── requirements.txt         # Dependências pip
├── top_features.json        # Features selecionadas (gerado após treinar)
│
├── README.md                # Documentação principal
├── SETUP.md                 # Este arquivo
├── ARCHITECTURE.md          # Arquitetura do projeto
├── API_DOCUMENTATION.md     # Documentação da API
├── FEATURES.md              # Descrição das features
├── DEVELOPMENT.md           # Guia de desenvolvimento
├── CONTRIBUTING.md          # Diretrizes de contribuição
└── LICENSE                  # Licença MIT
```

## ✅ Passo 4: Verificar Instalação

### 4.1 Testar importações Python

```bash
# Ativar venv (se não estiver ativado)
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux/Mac

# Testar importações
python -c "import pandas; print('pandas OK')"
python -c "import sklearn; print('sklearn OK')"
python -c "import fastapi; print('fastapi OK')"
python -c "import streamlit; print('streamlit OK')"
python -c "import mlflow; print('mlflow OK')"
```

Resposta esperada:
```
pandas OK
sklearn OK
fastapi OK
streamlit OK
mlflow OK
```

### 4.2 Verificar versões

```bash
python --version
pip list | grep -E "pandas|numpy|scikit-learn|fastapi|streamlit"
```

## 🚀 Passo 5: Treinar o Modelo

### 5.1 Executar treinamento

```bash
# Certificar que venv está ativado
.venv\Scripts\activate

# Executar script de treinamento
python src/train.py
```

### 5.2 Saída esperada

```
=== Step 1: Loading data with all numeric features ===
Total features available: 36
Features: ['MSSubClass', 'LotFrontage', ...]

=== Step 2: Training initial model with all features ===

=== Step 3: Extracting top 10 most important features ===
1. OverallQual: 0.5633
2. GrLivArea: 0.1246
...
10. GarageCars: 0.0139

Saved top 10 features to top_features.json

=== Step 4: Retraining model with only top 10 features ===

=== Final Model Performance (with top 10 features) ===
Mean Squared Error: 833076136.0117
R^2 Score: 0.8914
Mean Absolute Error: 18613.5778
Mean Absolute Percentage Error: 0.1156
```

### 5.3 Arquivos gerados

Após execução bem-sucedida, você terá:
- `mlruns/` - Diretório com artifacts do MLflow
- `mlflow.db` - Banco de dados SQLite com métricas/params
- `top_features.json` - Configuração das top 10 features
- Modelo treinado em pickle format

## 🖥️ Passo 6: Iniciar Servidores

### 6.1 API FastAPI (Terminal 1)

```bash
# Ativar venv
.venv\Scripts\activate

# Iniciar servidor
python src/serve.py
```

Saída esperada:
```
Warning: prometheus_client not available. Metrics will be disabled.
Loaded 10 top features from top_features.json
Model loaded from: mlruns\...\model.pkl
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 6.2 Interface Streamlit (Terminal 2)

```bash
# Ativar venv
.venv\Scripts\activate

# Iniciar interface
python -m streamlit run src/app.py
```

Saída esperada:
```
Welcome to Streamlit!

You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://XXX.XXX.X.X:8501
```

## 🌐 Passo 7: Acessar a Aplicação

### URLs Disponíveis

| Serviço | URL | Função |
|---------|-----|--------|
| **Streamlit UI** | http://localhost:8501 | Interface web para predições |
| **FastAPI Docs** | http://localhost:8000/docs | Documentação interativa da API |
| **API Health** | http://localhost:8000/health | Status do servidor |

### 7.1 Testar via Streamlit

1. Abrir http://localhost:8501 no navegador
2. Preencher os atributos do imóvel
3. Clicar em "Gerar Previsao"
4. Ver preço estimado

### 7.2 Testar via API (Command Line)

```bash
# Verificar saúde
curl http://localhost:8000/health

# Fazer predição
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [8, 2500, 2000, 500, 1000, 1500, 2500, 500, 2006, 2]}'
```

## 🐛 Troubleshooting

### Problema: "Python não encontrado"
**Solução:**
```bash
# Verificar instalação
where python  # Windows
which python  # Linux/Mac

# Se não encontrado, reinstalar Python
# Assegurar que "Add Python to PATH" está marcado
```

### Problema: "Poetry comando não encontrado"
**Solução:**
```bash
pip install poetry
poetry --version
```

### Problema: "Porta 8000/8501 já em uso"
**Solução:**
```bash
# Windows
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Problema: "ModuleNotFoundError"
**Solução:**
```bash
# Verificar venv está ativado
# (-ativado mostra (.venv) no prompt)

# Reinstalar dependências
pip install -r requirements.txt

# Ou com Poetry
poetry install
```

### Problema: "Streamlit não inicia"
**Solução:**
```bash
# Usar modo headless
set STREAMLIT_SERVER_HEADLESS=true  # Windows
export STREAMLIT_SERVER_HEADLESS=true  # Linux/Mac

python -m streamlit run src/app.py
```

### Problema: "Modelo não carrega"
**Solução:**
```bash
# Verificar se top_features.json e mlflow.db existem
dir top_features.json  # Windows
ls top_features.json   # Linux/Mac

# Se não existir, treinar novamente
python src/train.py
```

## 📊 Verificação Final

Para confirmar que tudo está funcionando:

```bash
# 1. Verificar estrutura
dir mlops-boston-project\  # Windows
ls -la mlops-boston-project/  # Linux/Mac

# 2. Verificar venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 3. Verificar dependências
pip list | head -20

# 4. Verificar datasets gerados
dir mlruns\  # Windows
ls mlruns/  # Linux/Mac

# 5. Verificar features
type top_features.json  # Windows
cat top_features.json  # Linux/Mac
```

## 📞 Próximos Passos

1. ✅ Ambiente configurado
2. ✅ Modelo treinado
3. ✅ Servidores rodando
4. ➡️ Explorar [ARCHITECTURE.md](ARCHITECTURE.md) - Entender a arquitetura
5. ➡️ Explorar [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Usar a API
6. ➡️ Explorar [DEVELOPMENT.md](DEVELOPMENT.md) - Desenvolver features novas

## 📚 Recursos Adicionais

- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [scikit-learn Guide](https://scikit-learn.org/stable/user_guide.html)

---

✅ Se chegou até aqui, seu ambiente está pronto! Prossiga para a próxima documentação.
