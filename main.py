from agent.graph import build_graph

graph = build_graph()


def create_initial_state():
    return {
        "user_query": "",
        "student_data": {},
        "subject": "",  

        "api_key": None,

        "intent": None,

        "prediction": None,
        "cluster": None,
        "metrics": {},

        "weak_areas": [],
        "reasoning": None,

        "difficulty": None,
        "trend": None,

        "study_plan": None,

        "retrieved_content": None,
        "course_recommendations": [],

        "history": [],

        "final_response": None
    }


state = create_initial_state()

# TEST DATA
state["user_query"] = "Why am I performing poorly?"

state["student_data"] = {
    "Quiz1": 40,
    "Quiz2": 35,
    "Quiz3": 30,
    "Time_Spent": 1,
    "Assignments": 2,
    "Attendance": 50
}


if not state.get("subject"):
    print("⚠️ No subject provided, using default for testing...")
    state["subject"] = "General Studies"

result = graph.invoke(state)

print(result.get("final_response"))