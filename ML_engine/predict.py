import pandas as pd
import random
import joblib

from resources_app.models import LearningResource

from ML_engine.config import (
    PROCESSED_STUDENTS,
    RESOURCES_DATASET,
    INTERACTIONS_DATASET,
    SIMILARITY_DATASET,
    MODEL_PATH
)

# =========================
# LOAD TRAINED MODEL
# =========================

model = joblib.load(MODEL_PATH)

# =========================
# LOAD DATASETS
# =========================

students = pd.read_csv(PROCESSED_STUDENTS)

resources = pd.read_csv(RESOURCES_DATASET)

interactions = pd.read_csv(INTERACTIONS_DATASET)

similarity = pd.read_csv(
    SIMILARITY_DATASET,
    index_col=0
)

# =========================
# FEATURE SETUP
# =========================

difficulty_map = {
    "Beginner": 0.2,
    "Intermediate": 0.5,
    "Advanced": 1.0
}

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
# HYBRID RECOMMENDATION
# =========================

def generate_recommendations(student_id):

    recs = list(
        set(content_based(student_id))
        |
        set(collaborative_based(student_id))
    )

    student = students.loc[student_id]

    ranked = []

    for r in recs:

        resource_match = resources[
            resources["resource_id"] == r
        ]

        if resource_match.empty:
            continue

        resource = resource_match.iloc[0]

        topic_match = (
            1
            if resource["topic"] == student["weak_topic"]
            else 0
        )

        difficulty = difficulty_map.get(
            resource["difficulty"],
            0.5
        )

        popularity = len(
            interactions[
                interactions["resource_id"] == r
            ]
        )

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

        score += random.uniform(
            0,
            0.02
        )

        try:

            db_resource = LearningResource.objects.get(
                title=resource["title"]
            )

            db_id = db_resource.id

        except Exception:

            continue

        ranked.append({
            "resource_id": db_id,
            "title": resource["title"],
            "topic": resource["topic"],
            "difficulty": resource["difficulty"],
            "type": resource["type"],
            "score": round(score, 4)
        })

    ranked = sorted(
        ranked,
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked