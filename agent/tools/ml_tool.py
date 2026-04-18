# agent/tools/ml_tool.py

import joblib
import numpy as np
import pandas as pd


# Load models once (global)
classifier = joblib.load("models/classifier.joblib")
scaler = joblib.load("models/scaler.joblib")

cluster_model = joblib.load("models/cluster_model.joblib")
cluster_scaler = joblib.load("models/cluster_scaler.joblib")

feature_columns = joblib.load("models/feature_columns.joblib")
column_means = joblib.load("models/column_means.joblib")
time_spent_bounds = joblib.load("models/time_spent_bounds.joblib")


def preprocess_input(data: dict):
    df = pd.DataFrame([data])

    # Fill missing values
    numeric_cols = [
        "Quiz1", "Quiz2", "Quiz3",
        "Time_Spent", "Assignments", "Attendance"
    ]

    for col in numeric_cols:
        if col not in df.columns:
            df[col] = column_means[col]

    df[numeric_cols] = df[numeric_cols].fillna(column_means)

    # Outlier handling (Time_Spent)
    df["Time_Spent"] = df["Time_Spent"].clip(
        time_spent_bounds["lower"],
        time_spent_bounds["upper"]
    )

    # Attendance clipping
    df["Attendance"] = df["Attendance"].clip(0, 100)

    return df

def feature_engineering(df):
    # Total Quiz Score
    df["Total_Quiz_Score"] = df["Quiz1"] + df["Quiz2"] + df["Quiz3"]

    # Average Quiz Score
    df["Average_Quiz_Score"] = df["Total_Quiz_Score"] / 3

    # Quiz Std (consistency)
    df["Quiz_Std"] = df[["Quiz1", "Quiz2", "Quiz3"]].std(axis=1)

    # Engagement Index
    df["Engagement_Index"] = (
        df["Time_Spent"] * 0.5 +
        df["Assignments"] * 0.3 +
        df["Attendance"] * 0.2
    )

    # Quiz Percentage
    df["Quiz_Percentage"] = (df["Total_Quiz_Score"] / 300) * 100

    # Effort Performance Ratio
    df["Effort_Performance_Ratio"] = (
        df["Total_Quiz_Score"] / (df["Time_Spent"] + 1)
    )

    return df

def predict_student(student_data: dict):
    # 1. Preprocess
    df = preprocess_input(student_data)

    # 2. Feature Engineering
    df = feature_engineering(df)

    # 3. Align columns
    df = df.reindex(columns=feature_columns, fill_value=0)

    # 4. Scale
    scaled = scaler.transform(df)

    # 5. Prediction
    pred = classifier.predict(scaled)[0]
    pred_label = "Pass" if pred == 1 else "Fail"

    avg_score = float(df["Average_Quiz_Score"].iloc[0])
    engagement = float(df["Engagement_Index"].iloc[0])
    time_spent = float(df["Time_Spent"].iloc[0])

    # Composite score: 60% quiz performance + 25% engagement + 15% time spent
    # Normalize: avg_score / 100 * 100, engagement is already 0-100 scale roughly,
    # time_spent normalize to 0-100 (assume 10 hrs max)
    normalized_time = min(time_spent / 10.0 * 100, 100)
    composite = avg_score * 0.60 + engagement * 0.25 + normalized_time * 0.15

    if avg_score >= 80 and composite >= 55:
        cluster_label = "High Performer"
    elif avg_score >= 40 and composite >= 30:
        cluster_label = "Average Performer"
    else:
        cluster_label = "At Risk"

    # 7. Metrics (for reasoning)
    metrics = {
        "avg_quiz_score": float(df["Average_Quiz_Score"].iloc[0]),
        "engagement_index": float(df["Engagement_Index"].iloc[0]),
        "quiz_std": float(df["Quiz_Std"].iloc[0]),
        "attendance": float(df["Attendance"].iloc[0]),
    }

    return {
        "prediction": pred_label,
        "cluster": cluster_label,
        "metrics": metrics
    }