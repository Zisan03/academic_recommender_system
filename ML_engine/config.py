from pathlib import Path

# =========================
# PROJECT ROOT DIRECTORY
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# DATASETS DIRECTORY
# =========================
DATASETS_DIR = BASE_DIR / "datasets"

STUDENT_DATASET = DATASETS_DIR / "student-mat.csv"

PROCESSED_STUDENTS = DATASETS_DIR / "processed_students.csv"

INTERACTIONS_DATASET = DATASETS_DIR / "interactions.csv"

SIMILARITY_DATASET = DATASETS_DIR / "student_similarity.csv"

RESOURCES_DATASET = DATASETS_DIR / "resources.csv"

# =========================
# RESULTS DIRECTORY
# =========================
RESULTS_DIR = BASE_DIR / "results"

METRICS_RESULTS = RESULTS_DIR / "metrics.csv"

CLASSIFICATION_RESULTS = RESULTS_DIR / "classification_report.csv"

RECOMMENDATION_RESULTS = RESULTS_DIR / "recommendations.csv"

# =========================
# TRAINED MODELS DIRECTORY
# =========================
MODELS_DIR = BASE_DIR / "trained_models"

MODEL_PATH = MODELS_DIR / "recommender.pkl"