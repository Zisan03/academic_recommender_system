import pandas as pd
import random

from ML_engine.config import (
    PROCESSED_STUDENTS,
    RESOURCES_DATASET,
    INTERACTIONS_DATASET
)

print(">>> INTERACTION SIMULATION STARTED <<<")

# =========================
# LOAD DATASETS
# =========================
students = pd.read_csv(PROCESSED_STUDENTS)

resources = pd.read_csv(RESOURCES_DATASET)

print("Datasets loaded successfully")

# =========================
# GENERATE INTERACTIONS
# =========================
interactions = []

for i, student in students.iterrows():

    student_id = i

    weak_topic = student["weak_topic"]

    # Get resources matching weak topic
    weak_resources = resources[
        resources["topic"] == weak_topic
    ]

    # Add weak-topic interactions
    sampled_resources = weak_resources.sample(
        min(2, len(weak_resources))
    )

    for _, res in sampled_resources.iterrows():

        interactions.append([
            student_id,
            res["resource_id"],
            1
        ])

    # Add random interactions
    random_resources = resources.sample(2)

    for _, res in random_resources.iterrows():

        interactions.append([
            student_id,
            res["resource_id"],
            1
        ])

# =========================
# CREATE DATAFRAME
# =========================
interaction_df = pd.DataFrame(
    interactions,
    columns=[
        "student_id",
        "resource_id",
        "interaction"
    ]
)

# =========================
# SAVE INTERACTIONS
# =========================
interaction_df.to_csv(
    INTERACTIONS_DATASET,
    index=False
)

print("Interactions generated successfully")

print(">>> INTERACTION SIMULATION COMPLETED <<<")


if __name__ == "__main__":
    print("Interaction simulator executed successfully.")