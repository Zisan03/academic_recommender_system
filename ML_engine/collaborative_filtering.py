import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from ML_engine.config import (
    INTERACTIONS_DATASET,
    SIMILARITY_DATASET
)

print(">>> COLLABORATIVE FILTERING STARTED <<<")

# =========================
# LOAD INTERACTION DATA
# =========================
interactions = pd.read_csv(
    INTERACTIONS_DATASET
)

print("Interactions loaded successfully")

# =========================
# CREATE USER-ITEM MATRIX
# =========================
user_item_matrix = interactions.pivot_table(
    index="student_id",
    columns="resource_id",
    values="interaction",
    fill_value=0
)

print("User-item matrix created")

# =========================
# COMPUTE STUDENT SIMILARITY
# =========================
similarity_matrix = cosine_similarity(
    user_item_matrix
)

# =========================
# CONVERT TO DATAFRAME
# =========================
similarity_df = pd.DataFrame(
    similarity_matrix,
    index=user_item_matrix.index,
    columns=user_item_matrix.index
)

print("Similarity matrix computed")

# =========================
# SAVE SIMILARITY MATRIX
# =========================
similarity_df.to_csv(
    SIMILARITY_DATASET
)

print("Similarity matrix saved successfully")

print(">>> COLLABORATIVE FILTERING COMPLETED <<<")


if __name__ == "__main__":
    print("Collaborative filtering module executed successfully.")