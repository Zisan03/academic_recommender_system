import pandas as pd
import random
import numpy as np

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
    SIMILARITY_DATASET,
    METRICS_RESULTS,
    CLASSIFICATION_RESULTS,
    RECOMMENDATION_RESULTS
)

print(">>> HYBRID MODEL STARTED <<<")

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

similarity = pd.read_csv(
    SIMILARITY_DATASET,
    index_col=0
)

print("All datasets loaded successfully")

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

# =========================
# CONTENT-BASED FILTERING
# =========================
def content_based(student_id):

    topic = students.loc[
        student_id,
        "weak_topic"
    ]

    return resources[
        resources["topic"] == topic
    ]["resource_id"].tolist()

# =========================
# COLLABORATIVE FILTERING
# =========================
def collaborative_based(student_id):

    similar_students = similarity.loc[
        student_id
    ].sort_values(
        ascending=False
    )[1:6].index

    recommended_resources = set()

    for sim_student in similar_students:

        sim_student = int(sim_student)

        items = interactions[
            interactions["student_id"] == sim_student
        ]["resource_id"].tolist()

        recommended_resources.update(items)

    return list(recommended_resources)

# =========================
# HYBRID RECOMMENDER
# =========================
def hybrid_ranked(student_id):

    recs = list(
        set(content_based(student_id))
        |
        set(collaborative_based(student_id))
    )

    student = students.loc[student_id]

    ranked = []

    for r in recs:

        resource = resources[
            resources["resource_id"] == r
        ].iloc[0]

        topic_match = 1 if (
            resource["topic"] == student["weak_topic"]
        ) else 0

        difficulty = difficulty_map[
            resource["difficulty"]
        ]

        popularity = len(
            interactions[
                interactions["resource_id"] == r
            ]
        )

        # =========================
        # FEATURE DATAFRAME
        # =========================
        features = pd.DataFrame([{
            "studytime": student["studytime"],
            "failures": student["failures"],
            "absences": student["absences"],
            "topic_match": topic_match,
            "difficulty": difficulty,
            "popularity": popularity
        }])

        score = model.predict_proba(
            features
        )[0][1]

        score += random.uniform(0, 0.02)

        ranked.append((r, score))

    ranked.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return ranked

# =========================
# GENERATE RECOMMENDATIONS
# =========================
student_id = 0

results = hybrid_ranked(student_id)

print(f"\nRanked Recommendations for Student {student_id}:\n")

print("Rank | Resource | Score")

print("--------------------------")

table_data = []

for i, (res, score) in enumerate(results, start=1):

    print(f"{i} | {res} | {score:.4f}")

    table_data.append([
        i,
        res,
        round(score, 4)
    ])

# =========================
# SAVE RECOMMENDATIONS
# =========================
rec_df = pd.DataFrame(
    table_data,
    columns=[
        "Rank",
        "Resource ID",
        "Score"
    ]
)

rec_df.to_csv(
    RECOMMENDATION_RESULTS,
    index=False
)

print("Recommendations saved successfully")

print("\n>>> HYBRID MODEL COMPLETED <<<")


if __name__ == "__main__":
    print("Hybrid recommendation engine executed successfully.")