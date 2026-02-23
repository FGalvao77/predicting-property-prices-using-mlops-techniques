import sys
import json
import types
import numpy as np
from pathlib import Path
import importlib.util


def make_fake_data_prep_module(path: Path):
    # Create a fake module named 'data_prep' that provides load_and_prepare_data
    mod = types.ModuleType('data_prep')

    def load_and_prepare_data(test_size=0.2, random_state=42, descr=False, selected_features=None):
        # If selected_features provided, use its length
        if selected_features is None:
            n_features = 12
            feature_names = [f'F{i}' for i in range(1, n_features + 1)]
        else:
            feature_names = selected_features
            n_features = len(selected_features)

        n_samples = 50
        # small random dataset
        rng = np.random.RandomState(0)
        X_train = rng.randn(int(n_samples * (1 - test_size)), n_features)
        X_test = rng.randn(int(n_samples * test_size), n_features)
        y_train = rng.randn(int(n_samples * (1 - test_size)))
        y_test = rng.randn(int(n_samples * test_size))
        return X_train, X_test, y_train, y_test, feature_names

    mod.load_and_prepare_data = load_and_prepare_data
    return mod


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_train_generates_top_features(tmp_path, monkeypatch):
    repo_root = Path.cwd()

    # inject fake data_prep into sys.modules before loading train.py
    fake_dp = make_fake_data_prep_module(repo_root)
    sys.modules['data_prep'] = fake_dp

    # create a dummy mlflow module to avoid real mlflow usage
    fake_mlflow = types.ModuleType('mlflow')
    class DummyRunCtx:
        def __enter__(self):
            return None
        def __exit__(self, exc_type, exc, tb):
            return False

    def start_run():
        return DummyRunCtx()

    fake_mlflow.start_run = start_run
    fake_mlflow.log_metric = lambda *a, **k: None
    fake_mlflow.log_param = lambda *a, **k: None
    fake_mlflow.set_tracking_uri = lambda *a, **k: None
    fake_mlflow.set_experiment = lambda *a, **k: None

    sklearn_mod = types.ModuleType('mlflow.sklearn')
    sklearn_mod.log_model = lambda *a, **k: None
    fake_mlflow.sklearn = sklearn_mod

    sys.modules['mlflow'] = fake_mlflow
    sys.modules['mlflow.sklearn'] = sklearn_mod

    # Load train.py as module and execute train_and_evaluate_model
    train_mod = load_module(Path('src') / 'train.py', 'train')

    # Run training (will produce top_features.json in repo root)
    train_mod.mlflow = fake_mlflow  # ensure module uses our fake
    train_mod.train_and_evaluate_model()

    cfg_path = repo_root / 'top_features.json'
    assert cfg_path.exists()
    data = json.loads(cfg_path.read_text())
    assert 'top_features' in data
    assert len(data['top_features']) == 10

    # cleanup
    try:
        cfg_path.unlink()
    except Exception:
        pass
