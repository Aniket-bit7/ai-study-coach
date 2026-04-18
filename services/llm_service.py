from groq import Groq
from agent.config import GROQ_API_KEY


def generate_response(prompt: str, api_key: str = None):
    """Generate LLM response using Groq. Accepts optional runtime API key."""
    key = api_key or GROQ_API_KEY

    if not key:
        return "⚠️ No Groq API key provided. Please enter your API key in the sidebar."

    client = Groq(api_key=key)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an intelligent and supportive AI study coach. Give concise, helpful, motivational answers. Use markdown formatting for readability."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content