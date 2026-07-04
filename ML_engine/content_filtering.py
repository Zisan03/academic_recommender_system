import pandas as pd

from ML_engine.config import (
    PROCESSED_STUDENTS,
    RESOURCES_DATASET
)

print(">>> CONTENT FILTERING STARTED <<<")

# =========================
# LOAD DATASETS
# =========================
students = pd.read_csv(
    PROCESSED_STUDENTS
)

resources = pd.read_csv(
    RESOURCES_DATASET
)

print("Datasets loaded successfully")

# =========================
# CONTENT-BASED RECOMMENDER
# =========================
def recommend_content(student_id):

    topic = students.loc[
        student_id,
        "weak_topic"
    ]

    recommendations = resources[
        resources["topic"] == topic
    ]

    return recommendations


# =========================
# TEST RECOMMENDATION
# =========================
student_id = 0

result = recommend_content(student_id)

print(f"\nRecommendations for Student {student_id}:")

print(result)

print("\n>>> CONTENT FILTERING COMPLETED <<<")


if __name__ == "__main__":
    print("Content filtering module executed successfully.")