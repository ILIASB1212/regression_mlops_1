from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionConfig:
    root_dir: Path
    dataset_download_url: Path
    load_dataset_lacation: Path
    upload_dataset_location: Path