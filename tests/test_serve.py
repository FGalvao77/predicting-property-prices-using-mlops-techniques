import os
import shutil
import json
import pickle
from pathlib import Path

from fastapi.testclient import TestClient
import importlib.util

# Load src/serve.py as a module (works even if `src` is not a package on sys.path)
spec = importlib.util.spec_from_file_location("serve", Path("src") / "serve.py")
serve = importlib.util.module_from_spec(spec)
import sys
sys.modules['serve'] = serve
spec.loader.exec_module(serve)


class DummyModel:
    def predict(self, X):
        # return sum of features as mock prediction
        return [float(X.sum())]


def setup_test_env(tmp_root: Path):
    # create mlruns structure
    artifacts_dir = tmp_root / "mlruns" / "test_run" / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # dump dummy model
    model_path = artifacts_dir / "model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(DummyModel(), f)

    # write top_features.json with 10 features
    cfg = {
        "top_features": [
            "F1",
            "F2",
            "F3",
            "F4",
            "F5",
            "F6",
            "F7",
            "F8",
            "F9",
            "F10",
        ],
        "feature_names": {f"F{i}": f"Feature {i}" for i in range(1, 11)},
    }
    with open(tmp_root / "top_features.json", "w", encoding="utf-8") as f:
        json.dump(cfg, f)

    return model_path, tmp_root / "top_features.json"


def teardown_test_env(tmp_root: Path):
    # remove mlruns and top_features.json
    shutil.rmtree(tmp_root / "mlruns", ignore_errors=True)
    try:
        (tmp_root / "top_features.json").unlink()
    except FileNotFoundError:
        pass


def test_health_and_predict(tmp_path):
    # prepare environment in repo root (tmp_path is isolated)
    repo_root = Path.cwd()
    # create test artifacts in repo working dir
    model_path, cfg_path = setup_test_env(repo_root)

    # reload serve module so it re-reads config and model files by re-executing its source
    import importlib.util
    spec = importlib.util.spec_from_file_location("serve", Path("src") / "serve.py")
    # update module spec and re-exec module code
    serve.__spec__ = spec
    spec.loader.exec_module(serve)

    client = TestClient(serve.app)

    # health should report model_loaded True and n_features 10
    r = client.get("/health")
    assert r.status_code == 200
    j = r.json()
    assert j.get("model_loaded") is True
    assert j.get("n_features") == 10

    # valid predict
    payload = {"features": [1] * 10}
    r2 = client.post("/predict", json=payload)
    assert r2.status_code == 200
    pred = r2.json().get("prediction")
    assert isinstance(pred, float)

    # invalid length
    r3 = client.post("/predict", json={"features": [1] * 5})
    assert r3.status_code == 400

    # cleanup
    teardown_test_env(repo_root)
