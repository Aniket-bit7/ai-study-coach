from agent.state import AgentState


def intent_node(state: AgentState):
    query = state.get("user_query", "").lower()

    if any(word in query for word in ["why", "reason", "problem", "weak", "poor", "failing", "bad"]):
        intent = "analysis"
    elif any(word in query for word in ["plan", "study", "schedule", "routine"]):
        intent = "planning"
    elif any(word in query for word in ["course", "learn", "resource", "video", "tutorial", "recommend"]):
        intent = "resources"
    elif any(word in query for word in ["next", "improve", "better", "advance", "ahead"]):
        intent = "next_steps"
    else:
        intent = "general"

    return {"intent": intent}