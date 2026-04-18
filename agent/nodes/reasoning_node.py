from agent.state import AgentState


def reasoning_node(state: AgentState):
    metrics = state.get("metrics", {})
    cluster = state.get("cluster", "")

    weak_areas = []
    reasons = []


    if metrics.get("engagement_index", 0) < 40:
        weak_areas.append("Low Engagement")
        reasons.append("You are not spending enough time studying.")


    if metrics.get("avg_quiz_score", 100) < 50:
        weak_areas.append("Low Quiz Performance")
        reasons.append("Your quiz scores are below average.")


    if metrics.get("quiz_std", 0) > 10:
        weak_areas.append("Inconsistent Performance")
        reasons.append("Your performance varies a lot between quizzes.")


    if metrics.get("attendance", 100) < 60:
        weak_areas.append("Low Attendance")
        reasons.append("Your attendance is too low.")


    if "At Risk" in cluster:
        reasons.append("You are in the At Risk category, which indicates low engagement.")

    reasoning_text = " ".join(reasons) if reasons else "Your performance is stable."

    return {
        "weak_areas": weak_areas,
        "reasoning": reasoning_text
    }