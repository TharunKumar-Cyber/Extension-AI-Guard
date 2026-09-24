from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PREPROCESSOR_PATH = (
    PROJECT_ROOT / "ml" / "preprocessing" / "artifacts" / "preprocessor.joblib"
)

MODEL_DIR = PROJECT_ROOT / "ml" / "models"

MODEL_PATHS = {
    "logistic_regression": MODEL_DIR / "logistic_regression.joblib",
    "decision_tree": MODEL_DIR / "decision_tree.joblib",
    "random_forest": MODEL_DIR / "random_forest.joblib",
    "svm": MODEL_DIR / "svm.joblib",
    "knn": MODEL_DIR / "knn.joblib",
    "gradient_boosting": MODEL_DIR / "gradient_boosting.joblib",
}

# Initial Phase 18 engineering configuration.
# This is configurable and does not declare a final production model.
DEFAULT_MODEL_NAME = "gradient_boosting"

FEATURE_SCHEMA_VERSION = "phase13-v1"

LABEL_MAPPING = {
    0: "BENIGN",
    1: "MALICIOUS",
}
