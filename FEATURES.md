# Features (Top 10)

Descrição das 10 features selecionadas automaticamente pelo pipeline de feature importance.

> Observação: as importâncias são valores gerados pelo `RandomForestRegressor` durante o treinamento final. Algumas importâncias são aproximadas quando não extraídas diretamente do último run.

## Lista ordenada (contrato)

1. `OverallQual` — Qualidade Geral (1-10)
2. `GrLivArea` — Área de Convivência (m²)
3. `TotalBsmtSF` — Área Total do Porão (m²)
4. `2ndFlrSF` — Área do 2º Andar (m²)
5. `BsmtFinSF1` — Área acabamento do porão 1 (m²)
6. `1stFlrSF` — Área do 1º Andar (m²)
7. `LotArea` — Área do Lote (ft²)
8. `GarageArea` — Área da Garagem (ft²)
9. `YearBuilt` — Ano de Construção (ano)
10. `GarageCars` — Vagas na Garagem (unidades)

---

## Detalhes por feature

- `OverallQual` (Qualidade Geral — 1-10)
  - Importance: 56.33%
  - Descrição: Avaliação qualitativa da construção/ acabamento geral.
  - Unidade: inteiros (1 = baixa, 10 = ótima)
  - Range esperado: 1 — 10
  - Exemplo: `8` → boa qualidade

- `GrLivArea` (Área de Convivência — m²)
  - Importance: 12.46%
  - Descrição: Área habitável acima do solo (living area).
  - Unidade: metros quadrados (m²)
  - Range típico: ~300 — 4000 (depende do dataset)
  - Exemplo: `2500`

- `TotalBsmtSF` (Área Total do Porão — m²)
  - Importance: 3.80%
  - Descrição: Soma das áreas do porão (acabadas + não acabadas).
  - Unidade: m²
  - Range típico: 0 — 2000
  - Exemplo: `1500`

- `2ndFlrSF` (Área do 2º Andar — m²)
  - Importance: ~3.5% (aproximado)
  - Descrição: Área útil do segundo pavimento.
  - Unidade: m²
  - Range típico: 0 — 1500
  - Exemplo: `500`

- `BsmtFinSF1` (Área Acabada do Porão 1 — m²)
  - Importance: ~3.2% (aproximado)
  - Descrição: Área acabada do tipo 1 no porão.
  - Unidade: m²
  - Range típico: 0 — 1500
  - Exemplo: `600`

- `1stFlrSF` (Área do 1º Andar — m²)
  - Importance: ~3.0% (aproximado)
  - Descrição: Área útil do primeiro pavimento.
  - Unidade: m²
  - Range típico: 300 — 2000
  - Exemplo: `1100`

- `LotArea` (Área do Lote — ft²)
  - Importance: ~3.0% (aproximado)
  - Descrição: Tamanho do terreno onde a casa está construída.
  - Unidade: pés quadrados (ft²) no dataset original
  - Range típico: 1300 — 215245
  - Exemplo: `7500`

- `GarageArea` (Área da Garagem — ft²)
  - Importance: ~3.0% (aproximado)
  - Descrição: Área construída da garagem.
  - Unidade: ft²
  - Range típico: 0 — 1500
  - Exemplo: `400`

- `YearBuilt` (Ano de Construção)
  - Importance: ~6.0% (aproximado)
  - Descrição: Ano em que a edificação foi construída. Impacta modernidade e desgaste.
  - Unidade: ano (YYYY)
  - Range típico: 1872 — 2010+
  - Exemplo: `2006`

- `GarageCars` (Vagas na Garagem)
  - Importance: ~5.7% (aproximado)
  - Descrição: Número de carros que cabem na garagem.
  - Unidade: contagem inteira
  - Range típico: 0 — 4
  - Exemplo: `2`

---

## Observações importantes

- Ordem e nomes técnicos são o contrato entre o cliente (UI) e o servidor; não reordene nem renomeie sem atualizar `top_features.json` e redeploy.
- Envie sempre valores brutos (sem scaling). O servidor aplica `StandardScaler` consistente com o treinamento.
- Ranges apresentados são baseados no dataset de treinamento; valores fora desses ranges podem produzir predições com maior incerteza.

---

Arquivo de configuração compartilhado: `top_features.json` — contém `top_features` (array ordenado) e `feature_names` (mapa técnico → friendly).

Próximo passo sugerido: gerar `DEVELOPMENT.md` com instruções para contribuir, executar testes e modificar o pipeline de features.