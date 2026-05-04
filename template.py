import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

list_of_files = [
    ".github/workflows/.gitkeep",              # fixed typo
    "src/loging/__init__.py",                  # no project_name, kept "loging"
    "src/loging/logger.py",
    "src/components/__init__.py",
    "src/utils/__init__.py",
    "src/utils/common.py",
    "src/config/__init__.py",
    "src/config/configuration.yaml",
    "src/pipeline/__init__.py",
    "src/entity/__init__.py",
    "src/entity/config_entity.py",
    "src/constants/__init__.py",
    "src/exceptions/__init__.py",
    "src/exceptions/custom_exceptions.py",
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    ".gitignore",
    "data",                                    # directory only
    "main.py",
    "Dockerfile",
    "docker-compose.yaml",
    "setup.py",
    "labs/lab.ipynb",
    "app.py"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir = filepath.parent
    filename = filepath.name

    # Create the directory if it doesn't exist
    if filedir != Path():
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory {filedir} for the file : {filename}")

    # Skip directory-only entries (like "data")
    if not filename:
        continue

    # Create empty file if it doesn't exist or is empty
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")