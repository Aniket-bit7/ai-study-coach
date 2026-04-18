import streamlit as st

def upload_section():
    st.subheader("📊 Student Data")

    col1, col2, col3 = st.columns(3)

    with col1:
        quiz1 = st.number_input("Quiz 1", 0, 100, 50)
        quiz2 = st.number_input("Quiz 2", 0, 100, 50)

    with col2:
        quiz3 = st.number_input("Quiz 3", 0, 100, 50)
        time_spent = st.number_input("Time Spent (hrs/day)", 0.0, 10.0, 2.0)

    with col3:
        assignments = st.number_input("Assignments Completed", 0, 10, 5)
        attendance = st.number_input("Attendance %", 0, 100, 75)


    subject = st.selectbox(
        "📘 Select Subject",
        [
            "Machine Learning",
            "Data Structures",
            "Mathematics",
            "DBMS",
            "Operating Systems",
            "Other"
        ]
    )

    if subject == "Other":
        subject = st.text_input("Enter subject")

    student_data = {
        "Quiz1": quiz1,
        "Quiz2": quiz2,
        "Quiz3": quiz3,
        "Time_Spent": time_spent,
        "Assignments": assignments,
        "Attendance": attendance
    }

    return student_data, subject