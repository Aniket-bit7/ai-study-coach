from agent.state import AgentState
from agent.tools.ml_tool import predict_student

def ml_node(state: AgentState):
    student_data = state.get("student_data", {})


    result = predict_student(student_data)

    return {
        "prediction": result["prediction"],
        "cluster": result["cluster"],
        "metrics": result["metrics"]
    }