import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Previous models
classifier = joblib.load(os.path.join(MODEL_DIR, "classifier.joblib"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.joblib"))
cluster_model = joblib.load(os.path.join(MODEL_DIR, "cluster_model.joblib"))
cluster_scaler = joblib.load(os.path.join(MODEL_DIR, "cluster_scaler.joblib"))
feature_columns = joblib.load(os.path.join(MODEL_DIR, "feature_columns.joblib"))
column_means = joblib.load(os.path.join(MODEL_DIR, "column_means.joblib"))
time_bounds = joblib.load(os.path.join(MODEL_DIR, "time_spent_bounds.joblib"))


def preprocess_input(data_dict):
    df = pd.DataFrame([data_dict])

    # Handle missing values
    df = df.fillna(column_means)

    # Clip values to valid ranges
    df["Time_Spent"] = df["Time_Spent"].clip(
        time_bounds["lower"], time_bounds["upper"]
    )
    df["Attendance"] = df["Attendance"].clip(0, 100)

    # Feature engineering
    df["Total_Quiz_Score"] = df["Quiz1"] + df["Quiz2"] + df["Quiz3"]
    df["Average_Quiz_Score"] = df["Total_Quiz_Score"] / 3
    df["Quiz_Std"] = df[["Quiz1", "Quiz2", "Quiz3"]].std(axis=1)

    df["Engagement_Index"] = (
        df["Time_Spent"] * 0.5 +
        df["Assignments"] * 0.3 +
        df["Attendance"] * 0.2
    )

    df["Quiz_Percentage"] = (df["Total_Quiz_Score"] / 300) * 100
    df["Effort_Performance_Ratio"] = (
        df["Total_Quiz_Score"] / (df["Time_Spent"] + 1)
    )

    df = df[feature_columns]

    return df

