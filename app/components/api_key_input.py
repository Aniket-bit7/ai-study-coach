import streamlit as st

def api_key_input():
    st.subheader("🔑 API Key")

    api_key = st.text_input(
        "Enter your Groq API Key",
        type="password"
    )

    return api_key