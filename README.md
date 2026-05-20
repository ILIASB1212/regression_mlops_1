# Bank Credit Risk MLOps Pipeline

A production-structured MLOps pipeline for credit risk classification using the German Credit Risk dataset. Built with modular architecture, multi-model experiment tracking, and a FastAPI serving layer.

---

## Project Overview

This project implements a full end-to-end machine learning pipeline for binary credit risk classification (good/bad) with MLOps best practices including experiment tracking, model versioning, containerization, and CI/CD automation.

**Dataset:** German Credit Risk (1000 records, 11 features)  
**Task:** Binary classification — predict whether a credit applicant is good or bad risk  
**Best models tested:** GradientBoosting, RandomForest, LogisticRegression, XGBoost

---

## Architecture

config/config.yaml          ← All paths and pipeline settings
params.yaml                 ← Model hyperparameters
schema.yaml                 ← Data schema and column types
↓
src/entity/config_entity.py ← Typed dataclasses for all configs
src/config/configuration.py ← ConfigurationManager — reads YAMLs, returns entities
↓
src/components/
data_ingestion.py       ← Downloads CSV from HuggingFace
data_validation.py      ← Validates columns against schema
data_transformation.py  ← Train/test split, saves artifacts
model_trainer.py        ← Multi-model training + MLflow tracking
model_evaluation.py     ← Final evaluation on held-out test set
↓
src/pipeline/run.py         ← PipeLine class — orchestrates all components
main.py                     ← Entry point
app.py                      ← FastAPI prediction endpoint

---

## Tech Stack

| Layer | Tool |
|---|---|
| ML Framework | scikit-learn, XGBoost |
| Experiment Tracking | MLflow + Dagshub |
| API Serving | FastAPI + Uvicorn |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Config Management | PyYAML + python-box |
| Data Source | HuggingFace Datasets |
| Testing | pytest |

---

## Pipeline Steps

**1. Data Ingestion**  
Downloads the German Credit Risk CSV directly from HuggingFace Hub and saves it to `artifacts/data_ingestion/`.

**2. Data Validation**  
Validates that all expected columns defined in `schema.yaml` are present in the raw data. Writes a validation status report to `artifacts/data_validation/status.txt`.

**3. Data Transformation**  
Splits data into train (85%) and test (15%) sets with a fixed random seed. Saves both splits to `artifacts/train/` and `artifacts/test/`.

**4. Model Training**  
Trains 4 models inside a full sklearn Pipeline (preprocessing + classifier):
- Numeric features: median imputation + StandardScaler
- Categorical features: most-frequent imputation + OneHotEncoder
- Models: GradientBoostingClassifier, RandomForestClassifier, LogisticRegression, XGBClassifier

Each model run is logged to MLflow/Dagshub with accuracy, F1 score, and model params. The best model by F1 score is saved to `artifacts/model/model.pkl`.

**5. Model Evaluation**  
Loads the saved best model and evaluates it on the held-out test set. Logs accuracy and F1 score.

---

## Project Structure

├── .github/
│   └── workflows/
│       └── ml-pipeline.yml     # CI/CD workflow
├── config/
│   └── config.yaml             # Pipeline configuration
├── src/
│   ├── components/             # Pipeline components
│   ├── config/                 # ConfigurationManager
│   ├── constants/              # File path constants
│   ├── entity/                 # Config dataclasses
│   ├── exceptions/             # Custom exception handler
│   ├── loging/                 # Logger setup
│   ├── pipeline/               # Pipeline orchestration
│   └── utils/                  # Shared utilities
├── test/
│   └── test_runer.py           # pytest tests
├── labs/
│   └── lab.ipynb               # Exploration notebook
├── app.py                      # FastAPI endpoint
├── main.py                     # Entry point
├── Dockerfile                  # Container definition
├── docker-compose.yaml         # Multi-service setup
├── params.yaml                 # Model hyperparameters
├── schema.yaml                 # Data schema
└── requirements.txt

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/ILIASB1212/regression_mlops_1.git
cd regression_mlops_1
```

### 2. Create and activate a virtual environment
```bash
python -m venv env
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the full training pipeline
```bash
python main.py
```

### 5. Start the prediction API
```bash
uvicorn app:apps --host 0.0.0.0 --port 8000
```

---

## API Usage

Once the server is running, visit `http://localhost:8000/docs` for the interactive Swagger UI.

**POST** `/predict`

Request body:
```json
{
  "Age": 35,
  "Sex": "male",
  "Job": 2,
  "Housing": "own",
  "Saving_accounts": "little",
  "Checking_account": "moderate",
  "Credit_amount": 3000,
  "Duration": 24,
  "Purpose": "car"
}
```

Response:
```json
{
  "risk": "good"
}
```

---

## Run with Docker

```bash
# Build and start
docker-compose up --build

# API will be available at http://localhost:8000
```

---

## Experiment Tracking

All training runs are tracked on Dagshub via MLflow:

- Metrics: accuracy, F1 score per model
- Parameters: model name, full hyperparameter dict
- Artifacts: fitted sklearn Pipeline (preprocessing + model)

View experiments at: `https://dagshub.com/ILIASB1212/regression_mlops_1`

---

## Run Tests

```bash
pytest test/ -v
```

Tests cover config loading, training data existence and schema, and model file integrity.

---

## Key Design Decisions

**Why sklearn Pipeline for the full preprocessor + model?**  
Ensures preprocessing is fitted only on training data and applied consistently at inference — no data leakage.

**Why F1 over accuracy for model selection?**  
The dataset is imbalanced (~70% good, ~30% bad). Accuracy is misleading; F1 properly penalizes missing the minority bad-risk class.

**Why multi-model training in one run?**  
Allows fair comparison of 4 models on identical train/test splits, with all results logged to MLflow for reproducibility.

---

## Author

**Ilias Baher** — AI/ML Engineer  
GitHub: [@ILIASB1212](https://github.com/ILIASB1212)  
Fiverr/Upwork: iliasbaher
