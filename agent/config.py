import os

try:
    import streamlit as st
    SERPAPI_KEY = st.secrets.get("SERPAPI_KEY", "")
except Exception:
    SERPAPI_KEY = ""

# 🔁 Fallback to environment variable (local)
if not SERPAPI_KEY:
    SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")