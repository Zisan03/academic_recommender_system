import pandas as pd
from sklearn.preprocessing import LabelEncoder

from ML_engine.config import (
    STUDENT_DATASET,
    PROCESSED_STUDENTS
)

print(">>> SCRIPT STARTED <<<")

# =========================
# LOAD DATASET
# =========================
data = pd.read_csv(STUDENT_DATASET, sep=';')

# Remove whitespace from column names
data.columns = data.columns.str.strip()

print("Dataset Loaded")
print(data.columns)

# =========================
# ENCODE CATEGORICAL COLUMNS
# =========================
categorical_cols = data.select_dtypes(include=['object']).columns

for col in categorical_cols:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])

print("Encoding Done")

# =========================
# CREATE WEAK STUDENT LABEL
# =========================
data["weak_student"] = data["G3"].apply(
    lambda x: 1 if x < 10 else 0
)

print("Weak student column created")

# =========================
# ASSIGN WEAK TOPICS
# =========================
def assign_topic(row):

    if row["failures"] > 1:
        return "Algebra"

    elif row["absences"] > 10:
        return "Statistics"

    elif row["studytime"] < 2:
        return "Programming"

    else:
        return "Calculus"


data["weak_topic"] = data.apply(assign_topic, axis=1)

print("Weak topics assigned")

# =========================
# SAVE PROCESSED DATASET
# =========================
data.to_csv(PROCESSED_STUDENTS, index=False)

print("Processed dataset saved successfully")

print(">>> PREPROCESSING COMPLETED <<<")


if __name__ == "__main__":
    print("Preprocessing module executed successfully.")