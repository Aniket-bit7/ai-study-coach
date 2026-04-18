from agent.state import AgentState
from rag.embedder import ChromaEmbedder


embedder = ChromaEmbedder()


def rag_node(state: AgentState):
    user_query = state.get("user_query", "")
    weak_areas = state.get("weak_areas", [])
    reasoning = state.get("reasoning", "")
    cluster = state.get("cluster", "")
    subject = state.get("subject", "")


    query_parts = []

    if weak_areas:
        query_parts.extend(weak_areas)

    if reasoning:
        query_parts.append(reasoning)

    if subject:
        query_parts.append(subject)


    if not query_parts:
        query_parts.append(user_query)

    smart_query = " ".join(query_parts)


    try:
        results = embedder.query(smart_query, n_results=5)
    except Exception:
        results = []


    filtered_results = []

    cluster_lower = cluster.lower()

    for doc in results:
        doc_lower = doc.lower()


        if "at risk" in cluster_lower:
            if weak_areas:
                if any(area.lower() in doc_lower for area in weak_areas):
                    filtered_results.append(doc)
            else:
                filtered_results.append(doc)


        elif "high performer" in cluster_lower:
            if "high performer" in doc_lower or "advanced" in doc_lower:
                filtered_results.append(doc)


        elif "struggling" in cluster_lower:
            if "concept" in doc_lower or "mistake" in doc_lower:
                filtered_results.append(doc)


        else:
            filtered_results.append(doc)


    if not filtered_results:
        filtered_results = results


    if filtered_results:
        content = "\n".join(filtered_results[:3])  
    else:
        content = "No relevant content found."

    return {
        "retrieved_content": content
    }