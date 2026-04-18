# agent/graph.py

from langgraph.graph import StateGraph, END

from agent.state import AgentState

from agent.nodes.intent_node import intent_node
from agent.nodes.ml_node import ml_node
from agent.nodes.reasoning_node import reasoning_node
from agent.nodes.adaptive_node import adaptive_node
from agent.nodes.planner_node import planner_node
from agent.nodes.rag_node import rag_node
from agent.nodes.search_node import search_node
from agent.nodes.response_node import response_node
from agent.nodes.llm_node import llm_node


def build_graph():
    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("intent", intent_node)
    graph.add_node("ml", ml_node)
    graph.add_node("reasoning", reasoning_node)
    graph.add_node("adaptive", adaptive_node)
    graph.add_node("planner", planner_node)
    graph.add_node("rag", rag_node)
    graph.add_node("search", search_node)   # 🔥 IMPORTANT
    graph.add_node("llm", llm_node)
    graph.add_node("response", response_node)

    # Flow
    graph.set_entry_point("intent")

    graph.add_edge("intent", "ml")
    graph.add_edge("ml", "reasoning")
    graph.add_edge("reasoning", "adaptive")
    graph.add_edge("adaptive", "planner")
    graph.add_edge("planner", "rag")
    graph.add_edge("rag", "search")    
    graph.add_edge("search", "llm")
    graph.add_edge("llm", "response")

    graph.add_edge("response", END)

    return graph.compile()