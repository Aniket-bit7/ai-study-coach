from agent.state import AgentState


def adaptive_node(state: AgentState):
    prediction = state.get("prediction")
    cluster = state.get("cluster", "")
    metrics = state.get("metrics", {})

    avg_score = metrics.get("avg_quiz_score", 0)
    engagement = metrics.get("engagement_index", 0)


    if prediction == "Fail" or "At Risk" in cluster:
        difficulty = "Easy"
        trend = "declining"


    elif avg_score >= 50 and engagement >= 40:
        difficulty = "Medium"
        trend = "improving"


    elif avg_score >= 75 and engagement >= 70:
        difficulty = "Hard"
        trend = "improving"

    else:
        difficulty = "Medium"
        trend = "stable"

    return {
        "difficulty": difficulty,
        "trend": trend
    }