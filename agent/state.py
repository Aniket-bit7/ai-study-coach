from typing import Dict, Any, List, Optional
from typing_extensions import TypedDict


class AgentState(TypedDict):

    user_query: str
    student_data: Dict[str, Any]
    subject: str                      # 🔥 NEW (MANDATORY)
    api_key: Optional[str]

    intent: Optional[str]

    prediction: Optional[str]
    cluster: Optional[str]
    metrics: Dict[str, Any]

    weak_areas: List[str]
    reasoning: Optional[str]

    difficulty: Optional[str]
    trend: Optional[str]

    study_plan: Optional[str]

    retrieved_content: Optional[str]

    course_recommendations: List[Dict[str, Any]]

    history: List[Dict[str, Any]]

    final_response: Optional[str]