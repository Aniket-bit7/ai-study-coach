# test_ml.py

from agent.tools.ml_tool import predict_student

student = {
    "Quiz1": 40,
    "Quiz2": 35,
    "Quiz3": 30,
    "Time_Spent": 1,
    "Assignments": 2,
    "Attendance": 50
}

result = predict_student(student)
print(result)