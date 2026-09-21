from pathlib import Path
import time

import joblib
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ARTIFACT_DIR = PROJECT_ROOT / "ml" / "preprocessing" / "artifacts"
MODEL_DIR = PROJECT_ROOT / "ml" / "models"

X_TRAIN_PATH = ARTIFACT_DIR / "X_train.csv"
Y_TRAIN_PATH = ARTIFACT_DIR / "y_train.csv"

RANDOM_STATE = 42


def load_training_data():
    """Load the Phase 13 training dataset."""
    X_train = pd.read_csv(X_TRAIN_PATH)
    y_train = pd.read_csv(Y_TRAIN_PATH).iloc[:, 0]

    return X_train, y_train


def build_models():
    """Build all Phase 14 classical ML models."""
    return {
        "logistic_regression": LogisticRegression(
            max_iter=1000,
            random_state=RANDOM_STATE,
        ),
        "decision_tree": DecisionTreeClassifier(
            random_state=RANDOM_STATE,
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=100,
            random_state=RANDOM_STATE,
        ),
        "svm": CalibratedClassifierCV(
            SVC(random_state=RANDOM_STATE),
            ensemble=False,
        ),
        "knn": KNeighborsClassifier(
            n_neighbors=5,
        ),
        "gradient_boosting": GradientBoostingClassifier(
            random_state=RANDOM_STATE,
        ),
    }


def main():
    """Train and save Phase 14 classical ML models."""
    print("=" * 60)
    print("PHASE 14 - CLASSICAL ML TRAINING")
    print("=" * 60)

    print("\nLoading Phase 13 training data...")
    X_train, y_train = load_training_data()

    print(f"X_train shape: {X_train.shape}")
    print(f"y_train shape: {y_train.shape}")
    print(
        f"Training labels: "
        f"{y_train.value_counts().sort_index().to_dict()}"
    )

    if X_train.isnull().any().any():
        raise ValueError("X_train contains missing values.")

    if y_train.isnull().any():
        raise ValueError("y_train contains missing values.")

    models = build_models()

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    training_times = {}

    for model_name, model in models.items():
        print(f"\nTraining: {model_name}")

        start_time = time.perf_counter()

        model.fit(X_train, y_train)

        training_time_sec = time.perf_counter() - start_time
        training_times[model_name] = training_time_sec

        model_path = MODEL_DIR / f"{model_name}.joblib"
        joblib.dump(model, model_path)

        print(
            f"  Training time: "
            f"{training_time_sec:.6f} sec"
        )
        print(f"  Saved: {model_path}")

    print("\n" + "=" * 60)
    print("TRAINING SUMMARY")
    print("=" * 60)

    for model_name, training_time in training_times.items():
        print(
            f"{model_name}: "
            f"{training_time:.6f} sec"
        )

    print("\nPHASE 14 CLASSICAL ML TRAINING: SUCCESS")


if __name__ == "__main__":
    main()