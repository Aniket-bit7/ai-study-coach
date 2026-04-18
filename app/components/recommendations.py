import streamlit as st

def show_recommendations(resources):
    if not resources:
        st.warning("No resources found")
        return

    st.subheader("🎓 Recommended Resources")

    for r in resources:
        with st.container():
            cols = st.columns([1, 3])


            if r.get("thumbnail"):
                cols[0].image(r["thumbnail"])


            cols[1].markdown(f"### [{r['title']}]({r['link']})")

            st.markdown("---")