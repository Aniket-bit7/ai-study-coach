from agent.state import AgentState


def planner_node(state: AgentState):
    difficulty = state.get("difficulty")
    weak_areas = state.get("weak_areas", [])

    plan = []


    if difficulty == "Easy":
        plan.append("Revise basic concepts for 1–2 hours daily")
        plan.append("Solve simple problems to build confidence")
        plan.append("Focus on understanding fundamentals clearly")


    elif difficulty == "Medium":
        plan.append("Practice moderate-level problems daily")
        plan.append("Revise weak concepts and analyze mistakes")
        plan.append("Take short quizzes to test understanding")


    elif difficulty == "Hard":
        plan.append("Solve advanced and challenging problems")
        plan.append("Participate in coding contests or timed tests")
        plan.append("Focus on optimization and speed")


    if "Low Engagement" in weak_areas:
        plan.append("Increase daily study time and maintain consistency")

    if "Low Quiz Performance" in weak_areas:
        plan.append("Focus on concept clarity and revise important topics")

    if "Low Attendance" in weak_areas:
        plan.append("Attend classes regularly and stay consistent")

    study_plan = "\n".join([f"- {p}" for p in plan])

    return {
        "study_plan": study_plan
    }