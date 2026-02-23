from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pickle
import time
import json
from pathlib import Path
from typing import Optional

try:
    from prometheus_client import Counter, Histogram, make_asgi_app
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    print('Warning: prometheus_client not available. Metrics will be disabled.')

# Create FastAPI app
app = FastAPI()

@app.get('/')
def root():
    return {
        'message': 'MLOps Boston House Price Prediction API',
        'endpoints': {
            'health': '/health',
            'predict': '/predict (POST)',
            'docs': '/docs'
        }
    }

# Setup Prometheus metrics if available
if PROMETHEUS_AVAILABLE:
    requests_total = Counter('requests_total', 'Total number of requests', ['method', 'endpoint'])
    request_duration = Histogram('request_duration_seconds', 'Duration of request processing in seconds', ['method', 'endpoint'])
    
    @app.middleware('http')
    async def metrics_middleware(request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        
        requests_total.labels(method=request.method, endpoint=request.url.path).inc()
        request_duration.labels(method=request.method, endpoint=request.url.path).observe(duration)
        return response
    
    # Mount metrics endpoint
    metrics_app = make_asgi_app()
    app.mount('/metrics', metrics_app)

# Load top features configuration
top_features = []
feature_names_map = {}
config_paths = [Path('../top_features.json'), Path('top_features.json')]
for config_path in config_paths:
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
            top_features = config.get('top_features', [])
            feature_names_map = config.get('feature_names', {})
        print(f'Loaded {len(top_features)} top features from {config_path}')
        break

if not top_features:
    print('Warning: top_features.json not found')

# Find the latest model saved (looking for the pickled sklearn model)
model = None
scaler: Optional[object] = None

# MLflow saves models in a specific directory structure
# Look for the model.pkl file in the mlruns hierarchy
model_candidates = list(Path('../mlruns').glob('**/model.pkl'))
if not model_candidates:
    model_candidates = list(Path('mlruns').glob('**/model.pkl'))

if model_candidates:
    # Use the most recently modified model file
    latest_model = max(model_candidates, key=lambda p: p.stat().st_mtime)
    try:
        with open(latest_model, 'rb') as f:
            model = pickle.load(f)
        print(f'Model loaded from: {latest_model}')
        # Try to locate a scaler (StandardScaler) near the model artifacts
        try:
            scaler_candidates = list(latest_model.parent.glob('**/*scaler*.pkl')) + list(latest_model.parent.glob('**/*StandardScaler*.pkl'))
            if not scaler_candidates:
                # fallback to searching mlruns root if not found next to model
                scaler_candidates = list(Path('../mlruns').glob('**/*scaler*.pkl')) + list(Path('mlruns').glob('**/*scaler*.pkl'))
            if scaler_candidates:
                scaler_path = max(scaler_candidates, key=lambda p: p.stat().st_mtime)
                try:
                    with open(scaler_path, 'rb') as sf:
                        scaler = pickle.load(sf)
                    print(f'Scaler loaded from: {scaler_path}')
                except Exception as e:
                    print(f'Warning: found scaler at {scaler_path} but failed to load: {e}')
        except Exception as e:
            print(f'Warning while searching for scaler: {e}')
    except Exception as e:
        print(f'Error loading model from {latest_model}: {e}')
else:
    print('Warning: No model.pkl found in mlruns directory')

class InputData(BaseModel):
    features: list[float]

@app.get('/health')
def health():
    return {
        'status': 'healthy', 
        'model_loaded': model is not None,
        'top_features': top_features,
        'n_features': len(top_features),
        'scaler_loaded': scaler is not None
    }

@app.post('/predict')
def predict(input_data: InputData):
    if model is None:
        raise HTTPException(status_code=500, detail='Model not loaded')

    if not top_features:
        raise HTTPException(status_code=500, detail='Feature configuration not loaded (top_features.json)')

    if len(input_data.features) != len(top_features):
        raise HTTPException(status_code=400, detail=f'Expected {len(top_features)} features, got {len(input_data.features)}')

    try:
        features_array = np.array(input_data.features).reshape(1, -1)
        if scaler is not None:
            try:
                features_array = scaler.transform(features_array)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f'Scaler transform error: {e}')

        prediction = model.predict(features_array)
        return {'prediction': float(prediction[0])}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)