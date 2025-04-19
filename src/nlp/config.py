from pathlib import Path

# Base directory (assumed project root)
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
KAGGLE_DATASET = "cornell-university/arxiv"
RAW_FILE_NAME = "arxiv-metadata-oai-snapshot.json"
PROCESSED_FILE_NAME = "arxiv-metadata-oai-snapshot.csv"

# Models
MODELS_DIR = BASE_DIR / "models"

# Reports, plots, metrics
REPORTS_DIR = BASE_DIR / "reports"
PLOTS_DIR = REPORTS_DIR / "plots"

# Create directories if needed
for path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR, REPORTS_DIR, PLOTS_DIR]:
    path.mkdir(parents=True, exist_ok=True)