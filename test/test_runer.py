import pytest
import os
import pandas as pd
from src.utils.common import read_yaml, load_model


def test_config_loads_correctly():
    """Test that config.yaml loads and has required keys"""
    config = read_yaml("config/config.yaml")
    assert hasattr(config, "artifacts_root")
    assert hasattr(config, "model_trainer")
    assert hasattr(config, "data_transformation")


def test_training_data_exists():
    """Test that the training CSV was created by the pipeline"""
    config = read_yaml("config/config.yaml")
    train_path = config.model_trainer.training_set
    assert os.path.exists(train_path), f"Training file not found at {train_path}"
    df = pd.read_csv(train_path)
    assert len(df) > 0, "Training file is empty"
    assert "Risk" in df.columns, "Target column 'Risk' missing from training data"


def test_model_file_exists_and_loads():
    """Test that the saved model exists and can be loaded"""
    config = read_yaml("config/config.yaml")
    model_path = config.model_trainer.model_path
    assert os.path.exists(model_path), f"Model file not found at {model_path}"
    model = load_model(model_path)
    assert model is not None, "Model loaded as None"
    assert hasattr(model, "predict"), "Loaded object has no predict method"