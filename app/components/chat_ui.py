import streamlit as st

def chat_ui():
    st.subheader("💬 Ask your question")

    query = st.text_input(
        "Example: Why am I weak? / Give me resources",
        placeholder="Type your question..."
    )

    return query