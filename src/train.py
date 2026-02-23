from data_prep import load_and_prepare_data

from sklearn.ensemble import RandomForestRegressor  
from sklearn.metrics import (mean_squared_error, 
                             r2_score, 
                             mean_absolute_error, 
                             mean_absolute_percentage_error)
import mlflow
import mlflow.sklearn
import json
import warnings

# Suppress specific warnings for cleaner output (MLflow 3.x & sklearn)
warnings.filterwarnings(action='ignore', category=UserWarning, module='sklearn')
warnings.filterwarnings(action='ignore', module='mlflow')

def train_and_evaluate_model():
   # Step 1: Load data with ALL numeric features
   print('\n=== Step 1: Loading data with all numeric features ===')
   X_train, X_test, y_train, y_test, all_feature_names = load_and_prepare_data()
   print(f'Total features available: {len(all_feature_names)}')
   print(f'Features: {all_feature_names}')

   # Step 2: Train initial model to identify important features
   print('\n=== Step 2: Training initial model with all features ===')
   initial_model = RandomForestRegressor(
      bootstrap=True, 
      max_depth=50,
      n_estimators=500, 
      n_jobs=-1,
      random_state=42
   )
   initial_model.fit(X=X_train, y=y_train)

   # Step 3: Get top 10 features based on feature importance
   print('\n=== Step 3: Extracting top 10 most important features ===')
   feature_importance = initial_model.feature_importances_
   importance_dict = {
      name: score for name, score in zip(all_feature_names, feature_importance)
   }
   sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
   
   top_10_features = [name for name, score in sorted_importance[:10]]
   for i, (name, score) in enumerate(sorted_importance[:10], 1):
      print(f'{i}. {name}: {score:.4f}')
   
   # Save top 10 features and their Brazilian Portuguese names to JSON
   feature_translations = {
      'OverallQual': 'Qualidade Geral (1-10)',
      'GrLivArea': 'Área de Convivência (m²)',
      'TotalBsmtSF': 'Área Total do Porão (m²)',
      'BsmtFinSF1': 'Área do Porão Acabada (m²)',
      '2ndFlrSF': 'Área do 2º Piso (m²)',
      '1stFlrSF': 'Área do 1º Piso (m²)',
      'LotArea': 'Tamanho do Terreno (m²)',
      'GarageCars': 'Capacidade da Garagem (Vagas)',
      'GarageArea': 'Área da Garagem (m²)',
      'YearBuilt': 'Ano de Construção',
      'FullBath': 'Banheiros Completos',
      'TotRmsAbvGrd': 'Total de Cômodos (acima do solo)',
      'YearRemodAdd': 'Ano de Remodelação',
      'Fireplaces': 'Lareiras',
      'LotFrontage': 'Frente do Terreno (m)',
      'WoodDeckSF': 'Área de Deck de Madeira (m²)',
      'OpenPorchSF': 'Área de Varanda Aberta (m²)'
   }
   
   features_config = {
      'top_features': top_10_features,
      'feature_names': {f: feature_translations.get(f, f) for f in top_10_features}
   }
   
   with open('top_features.json', 'w') as f:
      json.dump(features_config, f, indent=2)
   print(f'\nSaved top 10 features to top_features.json')

   # Step 4: Reload data with only top 10 features and retrain
   print('\n=== Step 4: Retraining model with only top 10 features ===')
   X_train_top10, X_test_top10, y_train_top10, y_test_top10, feature_names = \
      load_and_prepare_data(selected_features=top_10_features)
   
   # Train final model with top 10 features
   model = RandomForestRegressor(n_estimators=100, random_state=42)
   model.fit(X=X_train_top10, y=y_train_top10)

   # Make predictions
   y_pred = model.predict(X=X_test_top10)

   # Evaluate the model
   mse = mean_squared_error(y_true=y_test_top10, y_pred=y_pred)
   r2 = r2_score(y_true=y_test_top10, y_pred=y_pred)
   mae = mean_absolute_error(y_true=y_test_top10, y_pred=y_pred)
   mape = mean_absolute_percentage_error(y_true=y_test_top10, y_pred=y_pred)

   print(f'\n=== Final Model Performance (with top 10 features) ===')
   print('=' * 54)
   print('\t\tMETRICS')
   print(f'Mean Squared Error: {mse:.4f}')
   print(f'R^2 Score: {r2:.4f}')
   print(f'Mean Absolute Error: {mae:.4f}')
   print(f'Mean Absolute Percentage Error: {mape:.4f}')
   print('=' * 54 + '\n')

   # Log metrics with MLflow
   try:
      with mlflow.start_run():
         mlflow.log_metric('mse', mse)
         mlflow.log_metric('r2', r2)
         mlflow.log_metric('mae', mae)
         mlflow.log_metric('mape', mape)

         mlflow.log_param('model_type', 'RandomForestRegressor')
         mlflow.log_param('n_estimators', 100)
         mlflow.log_param('n_features', len(top_10_features))
         mlflow.log_param('top_features', ','.join(top_10_features))
         # Updated for MLflow 3.x compatibility
         mlflow.sklearn.log_model(sk_model=model, name='random_forest_model')
   except Exception as e:
      print(f'MLflow logging error: {e}')
      print('Model training completed without MLflow logging.')

if __name__ == '__main__':
   # Configure MLflow to use local SQLite database storage
   mlflow.set_tracking_uri(uri='sqlite:///mlflow.db')
   mlflow.set_experiment('House Price Prediction')
   
   train_and_evaluate_model()