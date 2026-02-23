# 🏗️ Arquitetura Técnica do Projeto

Este documento descreve a arquitetura, design patterns e fluxos de dados do projeto MLOps Boston House Price Prediction.

## 📐 Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                     CAMADA DE APRESENTAÇÃO                  │
│  ┌──────────────┐              ┌──────────────────────┐     │
│  │  Streamlit   │              │   FastAPI Swagger    │     │
│  │  Interface   │              │   Documentation      │     │
│  │  (Port 8501) │              │   (Port 8000/docs)   │     │
│  └──────────────┘              └──────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ HTTP/REST
                          │
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE API & SERVIDOR                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              FastAPI Application                       │ │
│  │  ├── /health → Status do servidor + features carregadas│ │
│  │  └── /predict → Fazer predições com 10 features       │ │
│  │                                                         │ │
│  │  Middleware:                                           │ │
│  │  ├── Prometheus Metrics (opcional)                    │ │
│  │  └── Request Logging                                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                       (Uvicorn Server)                      │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ Python/Pickle
                          │
┌─────────────────────────────────────────────────────────────┐
│                  CAMADA DE MODELO & LÓGICA                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │          Random Forest Regressor Model                 │ │
│  │                                                         │ │
│  │  - Treinado em: 80% dos dados                         │ │
│  │  - Testado em: 20% dos dados                          │ │
│  │  - Features: Top 10 selecionadas automaticamente      │ │
│  │  - Performance: R² = 0.8914                           │ │
│  │                                                         │ │
│  │  Feature Scaling:                                      │ │
│  │  └── StandardScaler normaliza inputs antes da predição│ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │     Top Features Configuration (JSON)                  │ │
│  │  - Carregado em tempo de inicialização                │ │
│  │  - Define 10 features esperadas pela API              │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ CSV/Pandas
                          │
┌─────────────────────────────────────────────────────────────┐
│                   CAMADA DE DADOS & TREINAMENTO             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  OpenML Dataset (Boston House Prices)                 │ │
│  │                                                         │ │
│  │  Processamento:                                        │ │
│  │  1. Carrega 506 instâncias × 81 features              │ │
│  │  2. Remove coluna 'Id'                                │ │
│  │  3. Seleciona apenas features numéricas (36)          │ │
│  │  4. Treina modelo inicial com todas                   │ │
│  │  5. Extrai importância das features                   │ │
│  │  6. Seleciona top 10 automaticamente                  │ │
│  │  7. Retreina modelo com top 10                        │ │
│  │  8. Salva em pickle format                            │ │
│  │  9. Registra em MLflow                                │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              MLflow Tracking                           │ │
│  │  - Armazena modelos treinados                         │ │
│  │  - Registra métricas e parâmetros                    │ │
│  │  - Mantém histórico de experimentos                   │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Fluxo de Dados

### 1. Fluxo de Treinamento (Training Pipeline)

```
┌──────────────────┐
│  OpenML Dataset  │
│  (506 x 81)      │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────┐
│  1. Data Preparation         │
│  - Remove 'Id'               │
│  - Seleciona 36 features     │
│  - Trata NaN values          │
│  - Split 80/20               │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  2. Initial Model Training   │
│  - Cria RF com 36 features   │
│  - Treina em 80% dados       │
│  - Calcula feature importance│
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  3. Feature Selection        │
│  - Rank features por score   │
│  - Seleciona top 10          │
│  - Salva em JSON             │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  4. Final Model Training     │
│  - Cria RF com 10 features   │
│  - Treina em 80% dados       │
│  - Calcula métricas          │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  5. Model Registry           │
│  - Salva em pickle format    │
│  - Registra no MLflow        │
│  - Documenta parâmetros      │
└──────────────────────────────┘
```

### 2. Fluxo de Predição (Inference Pipeline)

```
┌──────────────────────────────────┐
│  Streamlit Interface             │
│  - Usuário preenche 10 fields    │
│  - Clica "Gerar Previsao"        │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  HTTP POST /predict              │
│  Content-Type: application/json  │
│  Body: {"features": [v1...v10]}  │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  FastAPI Request Handler         │
│  - Valida número features (10)   │
│  - Valida tipos (float/int)      │
│  - Cria numpy array              │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Feature Scaling (StandardScaler)│
│  - Normaliza valores com fit     │
│  - Escala para distribuição ~N01 │
│  - Retorna (1, 10) array         │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Model Inference                 │
│  - Carrega modelo do pickle      │
│  - Executa predict() com dados   │
│  - Retorna valor numérico        │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  HTTP Response 200 OK            │
│  Body: {"prediction": 564320.51} │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Streamlit Display               │
│  - Mostra "Preco Estimado"       │
│  - Exibe em formato RS$ X.XXX,XX │
│  - Resumo dos atributos          │
└──────────────────────────────────┘
```

## 📁 Detalhamento dos Componentes

### **src/data_prep.py** - Preparação de Dados

```python
def load_and_prepare_data(
    test_size=0.2,           # Percentual teste
    random_state=42,         # Seed para reprodutibilidade
    descr=False,             # Exibir descrição dataset
    selected_features=None   # Features específicas
):
    """
    Pipeline de preparação de dados
    
    Fluxo:
    1. Carrega dataset OpenML (506 × 81)
    2. Remove 'Id' column
    3. Filtra apenas features numéricas (36)
    4. Seleciona features específicas se fornecidas
    5. Trata NaN com média
    6. Split train/test (80/20)
    7. StandardScaler normalization
    
    Retorna:
    - X_train_scaled: (405, n_features)
    - X_test_scaled: (101, n_features)
    - y_train: (405,)
    - y_test: (101,)
    - feature_names: list de strings
    """
```

### **src/train.py** - Treinamento e Feature Selection

```python
def train_and_evaluate_model():
    """
    Pipeline de treinamento com seleção automática
    
    Etapas:
    1. Load data com todas 36 features numéricas
    2. Treina RandomForest(n_estimators=100)
    3. Extrai feature_importances_
    4. Ranking e seleção top 10
    5. Salva config em top_features.json
    6. Retreina com apenas top 10
    7. Calcula métricas finais
    8. Registra em MLflow
    
    Output:
    - top_features.json (configuração)
    - mlruns/ (artifacts e modelos)
    - Métricas: MSE, R², MAE, MAPE
    """
```

### **src/serve.py** - API FastAPI

```python
class FastAPIApp:
    """
    Servidor ASGI para serving do modelo
    
    Componentes:
    - Carregamento do modelo em startup
    - Carregamento de features em startup
    - Middleware Prometheus (opcional)
    - Validação de inputs
    - Tratamento de erros
    
    Endpoints:
    - GET /health → {status, model_loaded, features, n_features}
    - POST /predict → {prediction} ou {error}
    """
```

### **src/app.py** - Interface Streamlit

```python
class StreamlitApp:
    """
    Interface web para predições
    
    Fluxo:
    1. Carrega configuração de features
    2. Cria inputs dinâmicos com Streamlit components
    3. Envia request POST para /predict
    4. Exibe resultado com formatação
    5. Mostra resumo dos atributos
    
    Componentes:
    - st.number_input para áreas
    - st.slider para qualidade (1-10)
    - st.expander para resumo
    """
```

## 🧮 Modelo de Machine Learning

### Random Forest Regressor

```
RandomForestRegressor(
    n_estimators=100,        # 100 árvores de decisão
    random_state=42,         # Seed reprodutível
    n_jobs=-1,               # Use all processors
    max_depth=None,          # Sem limite de profundidade
    min_samples_split=2,
    min_samples_leaf=1
)
```

### Treinamento

```
Dataset: 506 amostras × 10 features
Train: 405 (80%)
Test:  101 (20%)

Preprocessamento:
- StandardScaler: μ=0, σ=1

Validação:
- Test set (20%)
- Métricas: MSE, R², MAE, MAPE
```

## 📤 Endpoints da API

### GET /health

**Request:**
```bash
curl http://localhost:8000/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "top_features": [
    "OverallQual",
    "GrLivArea",
    ...
  ],
  "n_features": 10
}
```

### POST /predict

**Request:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [8, 2500, 2000, 500, 1000, 1500, 2500, 500, 2006, 2]
  }'
```

**Response (200 OK):**
```json
{
  "prediction": 564320.51
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Expected 10 features, got 9"
}
```

**Response (500 Internal Error):**
```json
{
  "error": "Model not loaded"
}
```

## 🔌 Integração entre Componentes

```
┌──────────────────────────────────────────────────────────┐
│                    Streamlit App                          │
│  - Lê top_features.json                                   │
│  - Cria UI dinâmica                                       │
│  - Envia HTTP POST para FastAPI                           │
└───────────────────┬──────────────────────────────────────┘
                    │
                    │ requests.post()
                    │ (HTTP JSON)
                    │
┌───────────────────▼──────────────────────────────────────┐
│                    FastAPI Server                         │
│  - Lê top_features.json                                   │
│  - Carrega modelo pickle                                  │
│  - Valida inputs                                          │
│  - Escala features com StandardScaler                     │
└───────────────────┬──────────────────────────────────────┘
                    │
                    │ numpy + sklearn
                    │
┌───────────────────▼──────────────────────────────────────┐
│                  Modelo ML                                │
│  - RandomForest com 100 trees                             │
│  - 10 features selecionadas                               │
│  - Retorna predição numérica                              │
└──────────────────────────────────────────────────────────┘
```

## 📊 Estrutura de Dados

### top_features.json

```json
{
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
  "feature_names": {
    "OverallQual": "Qualidade Geral (1-10)",
    "GrLivArea": "Area de Convivio (m2)",
    ...
  }
}
```

## 🎯 Padrões de Design Utilizados

### 1. **Pipeline Pattern**
- `data_prep.py` → `train.py` → `serve.py` → `app.py`
- Cada componente é independente e reutilizável

### 2. **Factory Pattern**
- `load_and_prepare_data()` cria datasets sob demanda
- Parâmetros permitem diferentes configurações

### 3. **Singleton Pattern**
- Modelo carregado uma vez e mantido em memória
- Features carregadas uma vez na inicialização

### 4. **Configuration Pattern**
- Parâmetros em `top_features.json`
- Facilita reutilização sem hardcoding

### 5. **REST Pattern**
- FastAPI segue REST conventions
- Separação clara entre recursos e operações

## 🔐 Considerações de Segurança

1. **Validação de Input**
   - Type checking em `/predict`
   - Range validation para features

2. **Error Handling**
   - Mensagens de erro genéricas
   - Logging de exceções

3. **Model Protection**
   - Modelo não é exposto diretamente
   - Acesso apenas via API

4. **Data Privacy**
   - Dados de entrada não são armazenados
   - Resposta apenas com predição

## 🚀 Performance

### Tempo de Resposta

```
Etapa                    Tempo
────────────────────────────
Load model              ~500ms (inicial)
Validate input          <1ms
Scale features          <1ms
Model prediction        <5ms
JSON serialization      <1ms
────────────────────────────
Total (warm start)      <10ms
```

### Escalabilidade

```
Scenario 1: Single request
- Latency: ~10ms
- Memory: ~200MB (model)

Scenario 2: Concurrent requests
- uvicorn workers: auto
- ThreadPoolExecutor: disponível
- Rate limiting: não implementado
```

## 📈 Métricas do Modelo

| Métrica | Valor | Interpretação |
|---------|-------|---------------|
| **R² Score** | 0.8914 | 89.14% variância explicada |
| **MAE** | R$ 18,613.58 | Erro médio absoluto |
| **MSE** | 833,076,136.01 | Erro quadrático médio |
| **MAPE** | 11.56% | Erro percentual médio |
| **Train/Test Split** | 80/20 | 405 train, 101 test |

## 🔄 Ciclo de Vida do Modelo

```
Development          Production
─────────────────────────────────────

Setup env ──→ Create venv
              Install deps
              
Train ──────→ Load data (36 features)
              Train initial RF
              Select top 10
              Retrain final RF
              Save to pickle
              Register in MLflow
              
Deploy ─────→ Start FastAPI
              Load model
              Load features config
              
Serve ──────→ Receive requests
              Validate inputs
              Predict
              Return results
              
Monitor ────→ Track metrics
              Log exceptions
              Alert on errors
```

---

**Próximos recursos:**
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Detalhes da API
- [FEATURES.md](FEATURES.md) - Explicação das features
- [DEVELOPMENT.md](DEVELOPMENT.md) - Desenvolvendo novas features
