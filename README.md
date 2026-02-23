# MLOps Boston House Price Prediction

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MLflow](https://img.shields.io/badge/mlflow-%23d9ead3.svg?style=for-the-badge&logo=mlflow&logoColor=blue)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![MIT License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

Um projeto _end-to-end_ de `Machine Learning` com foco em **MLOps**, demonstrando as melhores práticas de desenvolvimento, treinamento, serving e monitoramento de modelos de IA.

## 🎯 Objetivo

Criar um sistema de predição de preços de imóveis usando Random Forest, com arquitetura completa incluindo:

- Pipeline de preparação de dados
- Treinamento e seleção automática de features
- API REST para serving do modelo
- Interface web interativa
- Monitoramento com MLflow

## 🏗️ Arquitetura do Projeto

```
mlops-boston-project/
├── src/
│   ├── data_prep.py          # Preparação e processamento de dados
│   ├── train.py              # Treinamento do modelo e feature selection
│   ├── serve.py              # API FastAPI para serving do modelo
│   └── app.py                # Interface Streamlit
├── mlruns/                   # Artefatos do MLflow (modelos)
├── mlflow.db                 # Banco de dados SQLite do MLflow (métricas/params)
├── .venv/                    # Ambiente virtual Python
├── pyproject.toml            # Dependências Poetry
├── requirements.txt          # Dependências pip
├── top_features.json         # Configuração das top 10 features
├── README.md                 # Este arquivo
├── SETUP.md                  # Guia de configuração
├── ARCHITECTURE.md           # Documentação da arquitetura
├── API_DOCUMENTATION.md      # Documentação da API
└── FEATURES.md              # Descrição das features
```

## 🚀 Quick Start

### Pré-requisitos
- Python 3.13+
- Git
- Windows/Linux/Mac

### Instalação Rápida

```bash
# 1. Clonar o repositório
git clone https://github.com/seu-usuario/mlops-boston-project.git
cd mlops-boston-project

# 2. Criar ambiente virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux/Mac

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Treinar o modelo
python src/train.py

# 5. Iniciar servidores
# Terminal 1: FastAPI
python src/serve.py

# Terminal 2: Streamlit
python -m streamlit run src/app.py
```

Acesse a aplicação em **http://localhost:8501**

## 📚 Documentação do Projeto

Consulte os documentos detalhados:

- [Arquitetura](ARCHITECTURE.md)
- [Guia de Setup](SETUP.md)
- [Documentação da API](API_DOCUMENTATION.md)
- [Features (Top 10)](FEATURES.md)
- [Guia de Desenvolvimento](DEVELOPMENT.md)
- [Contribuição](CONTRIBUTING.md)
- [Código de Conduta](CODE_OF_CONDUCT.md)

Também há exemplos de requisições em `scripts/REQUEST_EXAMPLES.md`.

## 🐳 Docker & Docker Compose

Para construir as imagens e executar a aplicação (FastAPI + Streamlit) localmente via Docker Compose:

PowerShell (Windows):

```powershell
# Build images
docker compose build

# Start services (attached)
docker compose up

# Start services (background)
docker compose up -d

# Ver logs
docker compose logs -f api
docker compose logs -f web

# Parar e remover
docker compose down
```

Bash (Linux / macOS):

```bash
# Build
docker compose build

# Run (detached)
docker compose up -d

# Logs
docker compose logs -f api

# Stop
docker compose down
```

Notas:
- A API fica em `http://localhost:8000` e o front-end em `http://localhost:8501`.
- O volume `mlruns` persiste os artefatos do MLflow.
- As imagens usam `requirements.txt` para instalar dependências; em Windows certifique-se de que o Docker Desktop está ativo.

## ⚡ Atalhos e Scripts de Conveniência

Há atalhos para facilitar comandos Docker/Compose:

- `Makefile` — alvos disponíveis: `build`, `up`, `upd`, `logs-api`, `logs-web`, `down`.
- Scripts:
  - `scripts/start-dev.sh` (Bash) — build + up (detached)
  - `scripts/stop-dev.sh` (Bash) — down
  - `scripts/start-dev.ps1` (PowerShell) — build + up (detached)
  - `scripts/stop-dev.ps1` (PowerShell) — down

Exemplos:

PowerShell:

```powershell
# Start (PowerShell)
.\scripts\start-dev.ps1

# Stop
.\scripts\stop-dev.ps1
```

Bash (Linux/macOS):

```bash
# Start
bash scripts/start-dev.sh

# Stop
bash scripts/stop-dev.sh
```

Make (se disponível):

```bash
make build        # build images
make upd          # up detached
make logs-api     # follow API logs
make down         # stop and remove
```
## 📊 Componentes Principais

### 1. **Data Preparation** (`src/data_prep.py`)
- Carrega dataset de preços de imóveis (Boston House Prices)
- Remove colunas desnecessárias (ID)
- Seleciona apenas features numéricas
- Trata valores faltantes com média das colunas
- Padroniza features com StandardScaler
- Retorna datasets separados para treino/teste

### 2. **Model Training** (`src/train.py`)
- Treina modelo inicial com todas as features
- Extrai importância de cada feature
- Seleciona automaticamente top 10 features mais importantes
- Salva configuração em `top_features.json`
- Retreina modelo final apenas com top 10
- Registra métricas no MLflow

### 3. **Model Serving** (`src/serve.py`)
- API FastAPI na porta 8000
- Carrega modelo treinado e top features
- Endpoints:
  - `/health` - Status do servidor
  - `/predict` - Predição de preços
- Suporte opcional a Prometheus metrics

### 4. **Web Interface** (`src/app.py`)
- Interface Streamlit na porta 8501
- Inputs amigáveis em português
- Slider para qualidade geral
- Spinner inteligente para ano e capacidade garagem
- Resumo dos atributos enviados
- Exibição do preço estimado

## 📈 Performance do Modelo

| Métrica | Valor |
|---------|-------|
| R² Score | 0.8914 |
| Mean Absolute Error | R$ 18,613.58 |
| Mean Squared Error | 833,076,136.01 |
| MAPE | 11.56% |

## 🔧 Stack Tecnológico

| Componente | Tecnologia | Versão |
|-----------|-----------|--------|
| Linguagem | Python | 3.13 |
| ML Framework | scikit-learn | - |
| Data Processing | pandas, numpy | - |
| API | FastAPI, uvicorn | 1.54.0 |
| Web UI | Streamlit | 1.54.0 |
| Model Tracking | MLflow | - |
| Dependency Mgmt | Poetry | - |

## 📚 Top 10 Features para Predição

| Rank | Feature | Importância | Descrição |
|------|---------|------------|-----------|
| 1 | OverallQual | 56.33% | Qualidade Geral (1-10) |
| 2 | GrLivArea | 12.46% | Area de Convivio (m²) |
| 3 | TotalBsmtSF | 3.80% | Area do Porão (m²) |
| 4 | 2ndFlrSF | 3.57% | Area do 2º Piso (m²) |
| 5 | BsmtFinSF1 | 3.43% | Area Porão Acabada (m²) |
| 6 | 1stFlrSF | 2.99% | Area do 1º Piso (m²) |
| 7 | LotArea | 2.15% | Tamanho do Terreno (m²) |
| 8 | GarageArea | 1.90% | Area da Garagem (m²) |
| 9 | YearBuilt | 1.77% | Ano de Construção |
| 10 | GarageCars | 1.39% | Capacidade da Garagem |

## 🎓 Fluxo de Trabalho

### 1️⃣ Preparação do Ambiente
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ Treinamento do Modelo
```bash
python src/train.py
```
Outputs:
- Modelo treinado em `mlruns/`
- Métricas e parâmetros em `mlflow.db`
- Configuração de features em `top_features.json`

### 3️⃣ Iniciar API
```bash
python src/serve.py
```
API disponível em http://localhost:8000

### 4️⃣ Iniciar Interface Web
```bash
python -m streamlit run src/app.py
```
Interface disponível em http://localhost:8501

### 5️⃣ Fazer Predições
Via Streamlit ou via API:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [8, 2500, 2000, 500, 1000, 1500, 2500, 500, 2006, 2]}'
```

## 🧪 Testando a API

### Verificar saúde do servidor
```bash
curl http://localhost:8000/health
```

Resposta esperada:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "top_features": ["OverallQual", "GrLivArea", ...],
  "n_features": 10
}
```

### Fazer uma predição
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [8, 2500, 2000, 500, 1000, 1500, 2500, 500, 2006, 2]
  }'
```

Resposta esperada:
```json
{
  "prediction": 564320.51
}
```

## 📋 Requisitos do Sistema

### Hardware Mínimo
- CPU: 2 cores
- RAM: 4GB
- Disco: 500MB

### Hardware Recomendado
- CPU: 4+ cores
- RAM: 8GB+
- Disco: 1GB+

## 🔐 Segurança

- Não há dados sensíveis no repositório
- Models e artifacts estão em `.gitignore`
- Variáveis de ambiente devem ser configuradas

## 📝 Licença

Este projeto está sob licença MIT. Veja [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para instruções sobre como contribuir.

## 📚 Documentação Adicional

- [SETUP.md](SETUP.md) - Guia completo de configuração
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitetura detalhada
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Documentação API
- [FEATURES.md](FEATURES.md) - Descrição das features
- [DEVELOPMENT.md](DEVELOPMENT.md) - Guia de desenvolvimento

## 🆘 Troubleshooting

### Poetry comando não encontrado
```bash
# Reativar venv e instalar com pip
pip install poetry
```

### Porta 8000/8501 já em uso
```bash
# Encontrar e matar processo
Get-Process python | Stop-Process -Force
```

### Modelo não carrega
```bash
# Verificar se top_features.json existe
type top_features.json

# Treinar novamente
python src/train.py
```

## 👤 Autor

**Fernando Galvão**
- GitHub: [FGalvao77](https://github.com/FGalvao77)
- LinkedIn: [Fernando Galvão](https://www.linkedin.com/in/fernandocsgalvao/)

## 🙏 Agradecimentos

- Dataset: [OpenML - House Prices](https://www.openml.org/search?type=data&sort=runs&id=42165)
- Framework: scikit-learn, pandas, FastAPI, Streamlit
- ML Tracking: MLflow

---

⭐ Se este projeto foi útil, considere dar uma star 🌟
