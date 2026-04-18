from agent.state import AgentState


def response_node(state: AgentState):
    """
    Final node — passes through the LLM response.
    The LLM node already sets final_response,
    so we just return without overwriting it.
    """
    return {}