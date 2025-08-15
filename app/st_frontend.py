import streamlit as st
from quiz_logic import load_questions_from_json, calculate_orthodoxy_score

questions = load_questions_from_json(filepath='data/questions.json', need_validation=False)

st.title("Catholic Orthodoxy Quiz")
st.text("Welcome! Check your alignment with Catholic doctrine.")

user_answers = []
for i, q in enumerate(questions):
    st.subheader(f"Q{i+1}: {q['Question text']}")
    answer_labels = [ans[0] for ans in q['Answers']]
    choice = st.radio(
        label="Select your answer:",
        options=range(len(answer_labels)),
        format_func=lambda idx: answer_labels[idx],
        key=f"q{i}"
    )
    user_answers.append(choice)

if st.button("Submit"):
    score = calculate_orthodoxy_score(questions, user_answers)
    st.success(f"Your orthodoxy score: {score*100:.0f}%")