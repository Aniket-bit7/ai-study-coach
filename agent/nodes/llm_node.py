from agent.state import AgentState
from services.llm_service import generate_response
from agent.memory import get_formatted_history


def llm_node(state: AgentState):

    subject = state.get("subject", "Unknown")
    prediction = state.get("prediction", "N/A")
    cluster = state.get("cluster", "N/A")
    reasoning = state.get("reasoning", "")
    weak_areas = state.get("weak_areas", [])
    difficulty = state.get("difficulty", "N/A")
    study_plan = state.get("study_plan", "")
    guidance = state.get("retrieved_content", "")
    courses = state.get("course_recommendations", [])
    user_query = state.get("user_query", "")
    history = state.get("history", [])


    chat_history = get_formatted_history(history)


    resources_text = ""
    for r in courses:
        title = r.get("title", "")
        link = r.get("link", "")
        resources_text += f"- {title} ({link})\n"

    if not resources_text:
        resources_text = "No resources available."


    prompt = f"""
You are an intelligent, supportive, and friendly AI study coach.

Previous Conversation:
{chat_history}

Current User Question:
{user_query}

Student Context:
- Subject: {subject}
- Performance: {prediction}
- Category: {cluster}

Analysis:
{reasoning}

Weak Areas:
{", ".join(weak_areas) if weak_areas else "None"}

Difficulty Level:
{difficulty}

Study Plan:
{study_plan}

Learning Guidance:
{guidance}

Recommended Resources:
{resources_text}

Instructions:
- Respond like a mentor, not like a report
- Be conversational and motivating
- Explain clearly what the student should do next
- If user asked for resources, highlight them naturally
- Do NOT repeat raw structured data
"""


    api_key = state.get("api_key")

    final_response = generate_response(
        prompt=prompt,
        api_key=api_key
    )

    return {
        "final_response": final_response
    }