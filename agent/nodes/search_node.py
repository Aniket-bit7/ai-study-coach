from agent.state import AgentState
from services.search_service import search_courses


def search_node(state: AgentState):
    weak_areas = state.get("weak_areas", [])
    difficulty = state.get("difficulty")
    subject = state.get("subject")
    intent = state.get("intent")  


    if not subject:
        raise ValueError("Subject is required")


    results = search_courses(
        weak_areas=weak_areas,
        difficulty=difficulty,
        subject=subject,
        intent=intent  
    )

    return {
        "course_recommendations": results
    }