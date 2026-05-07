from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionConfig:
    root_dir: Path
    dataset_download_url: Path
    load_dataset_lacation: Path
    upload_dataset_location: Path


@dataclass
class DataValidationConfig:
    root_dir: Path
    local_data_file: Path
    status_folder: Path
    status_file: Path
    schemas: dict

@dataclass
class DataTransformationConfig:
    local_data_file: Path
    root_dir_train: Path
    root_dir_test: Path
    train_dir: Path
    test_dir :Path
    test_size: float
    random_state: int