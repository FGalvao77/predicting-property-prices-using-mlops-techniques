import pandas as pd
import numpy as np
from pathlib import Path
import importlib.util


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_load_and_prepare_numeric_selection(tmp_path):
    # Prepare a dummy housing Bunch-like object
    df = pd.DataFrame({
        'Id': [1, 2, 3, 4, 5],
        'num1': [1.0, 2.0, np.nan, 4.0, 5.0],
        'num2': [10, 20, 30, 40, 50],
        'cat': ['a', 'b', 'a', 'b', 'c']
    })
    target = np.array([100, 150, 200, 250, 300])

    class Bunch:
        pass

    bunch = Bunch()
    bunch.data = df
    bunch.feature_names = list(df.columns)
    bunch.target = target
    bunch.DESCR = 'dummy'

    # Load data_prep module and monkeypatch fetch_openml
    mod = load_module(Path('src') / 'data_prep.py', 'data_prep')
    mod.fetch_openml = lambda name, as_frame=True: bunch

    X_train, X_test, y_train, y_test, feature_names = mod.load_and_prepare_data(test_size=0.4, random_state=0)

    # Should select only numeric columns (num1, num2) and drop Id
    assert 'num1' in feature_names and 'num2' in feature_names
    assert 'Id' not in feature_names

    # Check shapes: 5 samples with test_size=0.4 -> train 3, test 2
    assert X_train.shape[0] == 3
    assert X_test.shape[0] == 2
    assert y_train.shape[0] == 3
    assert y_test.shape[0] == 2
