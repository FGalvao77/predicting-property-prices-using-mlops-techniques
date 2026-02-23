import streamlit as st
import requests
import json
from pathlib import Path

st.set_page_config(page_title='Predição de Preços', layout='wide')

st.title('PREDIÇÃO DE PREÇO DE IMÓVEL')
st.markdown('Insira as caracteristicas do imovel para obter uma previsão de preço')

# Load top features from configuration
top_features = []
feature_names_map = {}
config_paths = [Path('../top_features.json'), Path('top_features.json')]
for config_path in config_paths:
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
            top_features = config.get('top_features', [])
            feature_names_map = config.get('feature_names', {})
        break

if not top_features:
    st.error('Configuracao de features nao encontrada. Execute o treinamento do modelo primeiro!')
    st.stop()

st.info(f'Utilizando os {len(top_features)} atributos mais importantes para a previsao')

# Create input fields with friendly names
st.markdown('---')
st.subheader('Caracteristicas do Imovel')

feature_values = {}
cols = st.columns(2)  # 2-column layout for better UX
for i, feature_key in enumerate(top_features):
    col = cols[i % 2]
    friendly_name = feature_names_map.get(feature_key, feature_key)
    
    # Set appropriate input parameters based on feature type
    if feature_key == 'YearBuilt':
        feature_values[i] = col.number_input(
            friendly_name, 
            value=1980, 
            min_value=1800, 
            max_value=2026,
            key=f'feature_{i}'
        )
    elif feature_key == 'OverallQual':
        feature_values[i] = col.slider(
            friendly_name,
            min_value=1,
            max_value=10,
            value=5,
            key=f'feature_{i}'
        )
    elif feature_key == 'GarageCars':
        feature_values[i] = col.number_input(
            friendly_name,
            value=0,
            min_value=0,
            max_value=5,
            key=f'feature_{i}'
        )
    else:
        feature_values[i] = col.number_input(
            friendly_name,
            value=0.0,
            min_value=0.0,
            key=f'feature_{i}',
            step=100.0
        )

st.markdown('---')

# Prediction button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button('Gerar Previsao', use_container_width=True):
        input_data = {'features': [feature_values[i] for i in range(len(top_features))]}
        try:
            response = requests.post('http://localhost:8000/predict', json=input_data)
            if response.status_code == 200:
                result = response.json()
                if 'error' in result:
                    st.error(f'Erro: {result["error"]}')
                else:
                    prediction = result.get('prediction')
                    st.success(f'Preco Estimado: **R$ {prediction:,.2f}**')
                    
                    # Display feature summary
                    with st.expander('Resumo dos Atributos'):
                        summary_data = []
                        for i, feature_key in enumerate(top_features):
                            friendly_name = feature_names_map.get(feature_key, feature_key)
                            summary_data.append({
                                'Atributo': friendly_name,
                                'Valor': f'{feature_values[i]:.2f}' if not isinstance(feature_values[i], int) else str(feature_values[i])
                            })
                        st.table(summary_data)
            else:
                st.error(f'Erro no servidor: {response.status_code}')
        except Exception as e:
            st.error(f'Erro de conexao com a API: {e}')