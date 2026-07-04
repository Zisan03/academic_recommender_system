import pandas as pd
import shap

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

from ML_engine.config import (
    PROCESSED_STUDENTS,
    RESOURCES_DATASET,
    INTERACTIONS_DATASET
)

print(">>> EXPLAINABILITY MODULE STARTED <<<")

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
# TRAIN MODEL
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2
)

model = GradientBoostingClassifier()

model.fit(
    X_train,
    y_train
)

print("Model trained successfully")

# =========================
# SHAP EXPLAINABILITY
# =========================
explainer = shap.Explainer(
    model,
    X_train
)

shap_values = explainer(
    X_test
)

print("SHAP values generated successfully")

# =========================
# DISPLAY FEATURE IMPORTANCE
# =========================
print("\nGenerating SHAP summary plot...")

shap.plots.bar(
    shap_values
)

print("\n>>> EXPLAINABILITY COMPLETED <<<")


if __name__ == "__main__":
    print("Explainability module executed successfully.")