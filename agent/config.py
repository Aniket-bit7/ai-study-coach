import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Try Streamlit secrets first
try:
    import streamlit as st
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
    SERPAPI_KEY = st.secrets.get("SERPAPI_KEY")
except:
    GROQ_API_KEY = None
    SERPAPI_KEY = None

# Fallback to env
GROQ_API_KEY = GROQ_API_KEY or os.getenv("GROQ_API_KEY")
SERPAPI_KEY = SERPAPI_KEY or os.getenv("SERPAPI_KEY")