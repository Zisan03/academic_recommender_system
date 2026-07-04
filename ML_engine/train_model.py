import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    mean_squared_error
)

from ML_engine.config import (
    PROCESSED_STUDENTS,
    RESOURCES_DATASET,
    INTERACTIONS_DATASET,
    METRICS_RESULTS,
    CLASSIFICATION_RESULTS,
    MODEL_PATH
)

print(">>> MODEL TRAINING STARTED <<<")

# =========================
# LOAD DATASETS
# =========================
students = pd.read_csv(
    PROCESSED_STUDENTS
)

resources = pd.read_csv(
    RESOURCES_DATASET
)

interactions = pd.read_csv(
    INTERACTIONS_DATASET
)

print("Datasets loaded successfully")

# =========================
# FEATURE SETUP
# =========================
difficulty_map = {
    "Beginner": 0.2,
    "Intermediate": 0.5,
    "Advanced": 1.0
}

# =========================
# CREATE TRAINING DATA
# =========================
training_data = []

for i, student in students.iterrows():

    for _, resource in resources.iterrows():

        topic_match = 1 if (
            resource["topic"] == student["weak_topic"]
        ) else 0

        difficulty = difficulty_map[
            resource["difficulty"]
        ]

        popularity = len(
            interactions[
                interactions["resource_id"] == resource["resource_id"]
            ]
        )

        training_data.append([
            student["studytime"],
            student["failures"],
            student["absences"],
            topic_match,
            difficulty,
            popularity,
            student["weak_student"]
        ])

training_df = pd.DataFrame(
    training_data,
    columns=[
        "studytime",
        "failures",
        "absences",
        "topic_match",
        "difficulty",
        "popularity",
        "label"
    ]
)

# =========================
# FEATURE MATRIX
# =========================
X = training_df[
    [
        "studytime",
        "failures",
        "absences",
        "topic_match",
        "difficulty",
        "popularity"
    ]
]

y = training_df["label"]

# =========================
# TRAIN-TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2
)

# =========================
# TRAIN MODEL
# =========================
model = GradientBoostingClassifier()

model.fit(
    X_train,
    y_train
)

print("Model trained successfully")

# =========================
# SAVE TRAINED MODEL
# =========================
joblib.dump(
    model,
    MODEL_PATH
)

print(f"Model saved successfully at: {MODEL_PATH}")

# =========================
# MODEL EVALUATION
# =========================
y_pred = model.predict(X_test)

y_pred_proba = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred
)

recall = recall_score(
    y_test,
    y_pred
)

f1 = f1_score(
    y_test,
    y_pred
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred_proba
    )
)

print("\n=== MODEL PERFORMANCE ===")

print(f"Accuracy: {accuracy:.4f}")

print(f"Precision: {precision:.4f}")

print(f"Recall: {recall:.4f}")

print(f"F1 Score: {f1:.4f}")

print(f"RMSE: {rmse:.4f}")

# =========================
# SAVE METRICS
# =========================
metrics_df = pd.DataFrame({
    "Metric": [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "RMSE"
    ],
    "Value": [
        accuracy,
        precision,
        recall,
        f1,
        rmse
    ]
})

metrics_df.to_csv(
    METRICS_RESULTS,
    index=False
)

print("Metrics saved successfully")

# =========================
# SAVE CLASSIFICATION REPORT
# =========================
report = classification_report(
    y_test,
    y_pred,
    output_dict=True
)

report_df = pd.DataFrame(report).transpose()

report_df.to_csv(
    CLASSIFICATION_RESULTS
)

print("Classification report saved successfully")

print("\n>>> MODEL TRAINING COMPLETED <<<")


if __name__ == "__main__":
    print("Training pipeline executed successfully.")