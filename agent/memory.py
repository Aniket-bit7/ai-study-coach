def initialize_memory():
    return []


def add_to_memory(history, user_query, response):
    history.append({
        "user": user_query,
        "assistant": response
    })
    return history


def get_formatted_history(history):
    formatted = ""

    for chat in history:
        formatted += f"User: {chat['user']}\n"
        formatted += f"Assistant: {chat['assistant']}\n\n"

    return formatted